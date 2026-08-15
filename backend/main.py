from datetime import datetime, timedelta, timezone
from typing import Optional
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from supabase import create_client, Client

load_dotenv(Path(__file__).with_name('.env'))

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://xdvibkvbzuvsiainjujt.supabase.co')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhkdmlia3ZienV2c2lhaW5qdWp0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NjcxODYxOCwiZXhwIjoyMTAyMjk0NjE4fQ.ag2-CDHp4zTcvcoxeDZNY1gE1FZvFNO-bgCEWJtdjNI')
JWT_SECRET=('6f579b0e-63c3-41d3-8e3d-5ed1b8da2e4f')
JWT_SECRET = os.getenv('JWT_SECRET', '6f579b0e-63c3-41d3-8e3d-5ed1b8da2e4f')
JWT_EXPIRE_MINUTES = int(os.getenv('JWT_EXPIRE_MINUTES', '1440'))
CORS_ORIGINS = [x.strip() for x in os.getenv('CORS_ORIGINS', 'http://127.0.0.1:5500,http://localhost:5500').split(',') if x.strip()]

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    # App still starts so /docs can be inspected; database endpoints return a clear configuration error.
    supabase: Optional[Client] = None
else:
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

app = FastAPI(title='AgroTech API', version='1.0.0', description='AgroTech FastAPI + Supabase backend')
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS if CORS_ORIGINS != ['*'] else ['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
pwd = CryptContext(schemes=['bcrypt'], deprecated='auto')

class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=6, max_length=128)
    location: str = ''
    role: str = 'farmer'

class LoginIn(BaseModel):
    username: str
    password: str

class ProductIn(BaseModel):
    name: str
    category: str
    price: float
    unit: str
    description: str = ''
    image: str = ''
    rating: float = 0
    reviews: int = 0
    available: bool = True
    location: str = ''

class ServiceIn(BaseModel):
    name: str
    category: str
    price: float
    unit: str
    description: str
    location: str = ''
    image: str = ''
    available: bool = True

class OrderIn(BaseModel):
    product_id: int
    product_name: str
    quantity: int = Field(default=1, ge=1)
    price: float
    payment_method: str
    address: str
    notes: str = ''

class ComplaintIn(BaseModel):
    subject: str
    description: str
    priority: str = 'medium'

class NotificationIn(BaseModel):
    audience: str = 'all'
    message: str

class StatusIn(BaseModel):
    status: str


def db():
    if supabase is None:
        raise HTTPException(503, 'Supabase is not configured. Copy .env.example to .env and add your Supabase URL and service-role key.')
    return supabase


def make_token(user: dict):
    payload = {'sub': str(user['id']), 'role': user.get('role', 'farmer'), 'exp': datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)}
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')


def current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Missing Bearer token')
    try:
        payload = jwt.decode(authorization.split(' ', 1)[1], JWT_SECRET, algorithms=['HS256'])
        uid = payload.get('sub')
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Invalid or expired token')
    result = db().table('users').select('*').eq('id', uid).single().execute()
    if not result.data:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'User not found')
    if result.data.get('status') == 'blocked':
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Account is blocked')
    return result.data


def admin_user(user=Depends(current_user)):
    if user.get('role') != 'admin':
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Admin access required')
    return user

@app.get('/api/health')
def health():
    return {'status': 'ok', 'supabase_configured': supabase is not None}

@app.post('/api/auth/register')
def register(payload: RegisterIn):
    s = db()
    if payload.role not in {'farmer', 'seller'}:
        raise HTTPException(400, 'Public registration supports farmer or seller only')
    existing = s.table('users').select('id').eq('email', payload.email).execute().data
    if existing:
        raise HTTPException(409, 'Email already registered')
    row = {
        'name': payload.name, 'email': payload.email, 'phone': payload.phone,
        'password_hash': pwd.hash(payload.password), 'location': payload.location,
        'role': payload.role, 'status': 'active'
    }
    user = s.table('users').insert(row).execute().data[0]
    return {'message': 'Account created', 'user': {k: user[k] for k in ['id','name','email','phone','location','role','status']}, 'token': make_token(user)}

@app.post('/api/auth/login')
def login(payload: LoginIn):
    s = db()
    result = s.table('users').select('*').or_(f'email.eq.{payload.username},name.eq.{payload.username}').limit(1).execute()
    users = result.data or []
    if not users or not pwd.verify(payload.password, users[0]['password_hash']):
        raise HTTPException(401, 'Invalid credentials')
    user = users[0]
    if user.get('status') == 'blocked':
        raise HTTPException(403, 'Account is blocked')
    return {'message': 'Login successful', 'token': make_token(user), 'user': {k: user[k] for k in ['id','name','email','phone','location','role','status']}}

@app.get('/api/auth/me')
def me(user=Depends(current_user)):
    return {'user': {k: user[k] for k in ['id','name','email','phone','location','role','status']}}

@app.post('/api/admin/register')
def admin_register(payload: RegisterIn):
    s = db()
    existing = s.table('users').select('id').or_(f'email.eq.{payload.email},name.eq.{payload.name}').execute().data
    if existing:
        raise HTTPException(409, 'Admin already exists')
    row = {'name': payload.name, 'email': payload.email, 'phone': payload.phone or '0000000000', 'password_hash': pwd.hash(payload.password), 'location': payload.location, 'role': 'admin', 'status': 'active'}
    user = s.table('users').insert(row).execute().data[0]
    return {'message': 'Admin created', 'user': {k: user[k] for k in ['id','name','email','phone','location','role','status']}}

@app.post('/api/admin/login')
def admin_login(payload: LoginIn):
    response = login(payload)
    if response['user']['role'] != 'admin':
        raise HTTPException(403, 'Admin access required')
    return response

@app.get('/api/products')
def products(category: Optional[str] = None):
    q = db().table('products').select('*').order('id')
    if category and category.lower() != 'all': q = q.eq('category', category)
    return {'products': q.execute().data or []}

@app.post('/api/products')
def add_product(payload: ProductIn, user=Depends(admin_user)):
    return db().table('products').insert(payload.model_dump()).execute().data[0]

@app.put('/api/products/{product_id}')
def update_product(product_id: int, payload: ProductIn, user=Depends(admin_user)):
    res = db().table('products').update(payload.model_dump()).eq('id', product_id).execute().data
    if not res: raise HTTPException(404, 'Product not found')
    return res[0]

@app.delete('/api/products/{product_id}')
def delete_product(product_id: int, user=Depends(admin_user)):
    db().table('products').delete().eq('id', product_id).execute()
    return {'message': 'Product deleted'}

@app.get('/api/services')
def services(user=Depends(current_user)):
    res = db().table('services').select('*').eq('posted_by', user['id']).order('created_at', desc=True).execute()
    return {'services': res.data or []}

@app.post('/api/services')
def add_service(payload: ServiceIn, user=Depends(current_user)):
    row = {**payload.model_dump(), 'posted_by': user['id'], 'status': 'pending'}
    return db().table('services').insert(row).execute().data[0]

@app.put('/api/services/{service_id}')
def update_service(service_id: int, payload: ServiceIn, user=Depends(current_user)):
    res = db().table('services').update(payload.model_dump()).eq('id', service_id).eq('posted_by', user['id']).execute().data
    if not res: raise HTTPException(404, 'Service not found')
    return res[0]

@app.delete('/api/services/{service_id}')
def delete_service(service_id: int, user=Depends(current_user)):
    db().table('services').delete().eq('id', service_id).eq('posted_by', user['id']).execute()
    return {'message': 'Service deleted'}

@app.post('/api/orders')
def create_order(payload: OrderIn, user=Depends(current_user)):
    oid = 'AGT' + str(int(datetime.now().timestamp() * 1000))[-8:]
    row = {**payload.model_dump(), 'order_id': oid, 'user_id': user['id'], 'payment_status': 'pending', 'status': 'pending'}
    saved = db().table('orders').insert(row).execute().data[0]
    return saved

@app.get('/api/orders')
def my_orders(user=Depends(current_user)):
    res = db().table('orders').select('*').eq('user_id', user['id']).order('created_at', desc=True).execute()
    return {'orders': res.data or []}

@app.post('/api/complaints')
def create_complaint(payload: ComplaintIn, user=Depends(current_user)):
    return db().table('complaints').insert({**payload.model_dump(), 'user_id': user['id']}).execute().data[0]

@app.get('/api/notifications')
def notifications(user=Depends(current_user)):
    res = db().table('notifications').select('*').order('created_at', desc=True).limit(50).execute()
    return {'notifications': res.data or []}

@app.get('/api/admin/dashboard')
def admin_dashboard(user=Depends(admin_user)):
    s = db()
    users = s.table('users').select('id', count='exact').execute().count or 0
    products_count = s.table('products').select('id', count='exact').execute().count or 0
    services_count = s.table('services').select('id', count='exact').execute().count or 0
    orders = s.table('orders').select('id,price,status,payment_status').execute().data or []
    revenue = sum(float(x.get('price') or 0) for x in orders if x.get('payment_status') in {'paid','success','completed'} or x.get('status') == 'completed')
    return {'users': users, 'products': products_count, 'services': services_count, 'orders': len(orders), 'revenue': revenue, 'pending_orders': sum(1 for x in orders if x.get('status') == 'pending')}

@app.get('/api/admin/users')
def admin_users(user=Depends(admin_user)):
    return {'users': db().table('users').select('id,name,email,phone,location,role,status,created_at').order('created_at', desc=True).execute().data or []}

@app.put('/api/admin/users/{user_id}/status')
def admin_user_status(user_id: str, payload: StatusIn, user=Depends(admin_user)):
    if payload.status not in {'active','blocked','pending'}: raise HTTPException(400, 'Invalid status')
    res = db().table('users').update({'status': payload.status}).eq('id', user_id).execute().data
    if not res: raise HTTPException(404, 'User not found')
    return res[0]

@app.get('/api/admin/listings')
def admin_listings(user=Depends(admin_user)):
    services = db().table('services').select('*,users(name,email)').order('created_at', desc=True).execute().data or []
    return {'listings': services}

@app.put('/api/admin/listings/{listing_id}/status')
def admin_listing_status(listing_id: int, payload: StatusIn, user=Depends(admin_user)):
    if payload.status not in {'pending','approved','rejected'}: raise HTTPException(400, 'Invalid listing status')
    res = db().table('services').update({'status': payload.status}).eq('id', listing_id).execute().data
    if not res: raise HTTPException(404, 'Listing not found')
    return res[0]

@app.get('/api/admin/orders')
def admin_orders(user=Depends(admin_user)):
    return {'orders': db().table('orders').select('*,users(name,email)').order('created_at', desc=True).execute().data or []}

@app.put('/api/admin/orders/{order_id}/status')
def admin_order_status(order_id: str, payload: StatusIn, user=Depends(admin_user)):
    allowed = {'pending','confirmed','completed','cancelled'}
    if payload.status not in allowed: raise HTTPException(400, 'Invalid order status')
    res = db().table('orders').update({'status': payload.status}).eq('order_id', order_id).execute().data
    if not res: raise HTTPException(404, 'Order not found')
    return res[0]

@app.get('/api/admin/payments')
def admin_payments(user=Depends(admin_user)):
    rows = db().table('orders').select('order_id,price,payment_method,payment_status,status,created_at').order('created_at', desc=True).execute().data or []
    return {'payments': rows}

@app.get('/api/admin/complaints')
def admin_complaints(user=Depends(admin_user)):
    return {'complaints': db().table('complaints').select('*,users(name,email)').order('created_at', desc=True).execute().data or []}

@app.put('/api/admin/complaints/{complaint_id}/status')
def admin_complaint_status(complaint_id: int, payload: StatusIn, user=Depends(admin_user)):
    if payload.status not in {'open','assigned','resolved','closed'}: raise HTTPException(400, 'Invalid complaint status')
    res = db().table('complaints').update({'status': payload.status}).eq('id', complaint_id).execute().data
    if not res: raise HTTPException(404, 'Complaint not found')
    return res[0]

@app.post('/api/admin/notifications')
def admin_notification(payload: NotificationIn, user=Depends(admin_user)):
    return db().table('notifications').insert({'audience': payload.audience, 'message': payload.message, 'created_by': user['id']}).execute().data[0]
