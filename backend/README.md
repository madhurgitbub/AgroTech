# AgroTech Backend — FastAPI + Supabase

This folder contains the real backend for the AgroTech frontend.

## Stack
- FastAPI REST API
- Supabase PostgreSQL
- JWT authentication
- bcrypt password hashing
- Role-based admin authorization

## 1. Create Supabase database
1. Create a project at https://supabase.com/
2. Open **SQL Editor**.
3. Paste and run `schema.sql`.
4. Open **Project Settings → API** and copy the project URL and **service_role** key.
5. Never put the service_role key inside frontend JavaScript.

## 2. Configure environment
Copy `.env.example` to `.env` and fill in:

- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `JWT_SECRET`
- `CORS_ORIGINS`

## 3. Install and run
Windows:

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

Linux/macOS:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

API docs: `http://127.0.0.1:8000/docs`

## 4. Seed the existing AgroTech products
After configuring `.env`:

```bash
python seed.py
```

This imports the products from `../data/data.json` into Supabase if the products table is empty.

## 5. Run the frontend
From the project root:

```bash
python -m http.server 5500
```

Open:

`http://127.0.0.1:5500/`

The frontend API client defaults to:

`http://127.0.0.1:8000/api`

If your backend is deployed, run this in the browser console once before using the app:

```javascript
localStorage.setItem('agro_api_base', 'https://YOUR-BACKEND-DOMAIN/api');
```

Then reload the page.

## Important
- Do not commit `.env`.
- Do not expose `SUPABASE_SERVICE_ROLE_KEY` to the frontend.
- Public farmer/seller registration is available.
- Admin registration is kept as a separate page because the existing AgroTech UI requested separate Admin Login and Admin Register buttons. In production, admin registration should be protected by an invitation/super-admin approval flow.
