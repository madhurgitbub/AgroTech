# 🌾 AgroTech

## Smart Agricultural Marketplace & Equipment Rental Platform

> **AgroTech is a full-stack digital platform that connects farmers with agricultural equipment, products, and services — making farming resources easier to discover, rent, purchase, and manage.**

---

## 🌱 About The Project

Agriculture often involves challenges such as limited access to farming equipment, difficulty finding reliable agricultural services, and fragmented purchasing processes.

**AgroTech** addresses these challenges through a centralized digital platform where farmers can:

* 🚜 Discover agricultural equipment
* 🛒 Purchase farming products
* 🤝 Find agricultural services
* 📦 Manage orders and purchases
* ❤️ Save products to a wishlist
* 👤 Manage their profile
* 🔔 Receive notifications
* 🆘 Get help and support

The platform also provides a dedicated **Admin Panel** for managing users, products, services, orders, complaints, payments, and notifications.

---

# ✨ Key Features

## 👨‍🌾 Farmer Features

### 🔐 Authentication

* User registration
* User login
* Secure JWT authentication
* Protected user sessions
* Profile management

### 🔎 Product Discovery

* Product search
* Category filtering
* Sorting
* Product details
* Product specifications
* Reviews and ratings

### 🚜 Agricultural Services

* Browse available services
* Add new agricultural services
* Manage personal service listings
* Update service information
* Delete services
* Activate / deactivate listings

### 🛒 Orders & Purchases

* Purchase products
* Order management
* Purchase history
* Order status tracking
* Multiple payment options

### ❤️ Personalization

* Wishlist
* Notifications
* User profile
* Account management

### 🆘 Support

* FAQ section
* Hindi + English help content
* Support request system

---

# 🛡️ Admin Panel

AgroTech includes a dedicated administration system for controlling and monitoring the platform.

### Admin capabilities include:

* 📊 Dashboard
* 👥 User management
* 📦 Product management
* 🚜 Service management
* ✅ Service approval
* 🛒 Order management
* 💳 Payment monitoring
* ⚠️ Complaint management
* 🔔 Notification management
* 🔐 Role-based authorization

The admin panel provides centralized control over the complete platform.

---

# 🧠 System Architecture

```text
                    🌾 FARMER
                       │
                       ▼
              ┌─────────────────┐
              │   AgroTech UI   │
              │                 │
              │ HTML5           │
              │ CSS3            │
              │ JavaScript      │
              └────────┬────────┘
                       │
                       │ REST API
                       ▼
              ┌─────────────────┐
              │ FastAPI Backend │
              │                 │
              │ Authentication  │
              │ Products        │
              │ Services        │
              │ Orders          │
              │ Payments        │
              │ Admin           │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Supabase     │
              │   PostgreSQL    │
              │                 │
              │ Users           │
              │ Products        │
              │ Services        │
              │ Orders          │
              │ Complaints      │
              └─────────────────┘
```

---

# 🛠️ Technology Stack

## Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Responsive Web Design

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* JWT Authentication
* bcrypt

## Database

* Supabase
* PostgreSQL

## Development Tools

* Git
* GitHub
* VS Code
* Python Virtual Environment

---

# 📂 Project Structure

```text
AgroTech/
│
├── index.html
├── 404.html
├── RUN_PROJECT.md
├── requirements.txt
│
├── backend/
│   ├── main.py
│   ├── seed.py
│   ├── schema.sql
│   ├── requirements.txt
│   ├── run_backend.bat
│   └── README.md
│
├── css/
│   ├── global.css
│   ├── index.css
│   └── home.css
│
├── js/
│   ├── global.js
│   └── home.js
│
├── data/
│   └── data.json
│
└── pages/
    ├── login.html
    ├── register.html
    ├── home.html
    ├── search.html
    ├── product.html
    ├── buy.html
    ├── addService.html
    ├── my_services.html
    ├── my_purchase.html
    ├── myaccount.html
    ├── wishlist.html
    ├── notifications.html
    └── help.html
```

---

# 🔄 How The System Works

```text
User Registration
       ↓
User Login
       ↓
JWT Authentication
       ↓
Browse Products / Services
       ↓
Select Product or Service
       ↓
Place Order / Manage Service
       ↓
FastAPI Processes Request
       ↓
Supabase PostgreSQL
       ↓
Response Returned to User
```

---

# 🔐 Security

AgroTech implements several security practices:

* 🔑 JWT-based authentication
* 🔒 bcrypt password hashing
* 🛡️ Role-based access control
* 🔐 Environment-based secret management
* 🚫 Service-role database key is not exposed to frontend
* ✅ Protected backend routes
* ✔️ Pydantic request validation
* 🔒 Secure user sessions

---

# 📊 Major Modules

```text
┌──────────────────────────────┐
│       Authentication         │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│       User Management        │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│    Products & Equipment      │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│    Agricultural Services     │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│      Orders & Purchases      │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│   Payments & Notifications   │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│        Admin Panel           │
└──────────────────────────────┘
```

---

# 🚀 Running The Project

## Step 1 — Setup Backend

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Step 2 — Configure Environment

Create:

```text
backend/.env
```

Add your configuration:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
JWT_SECRET=your_jwt_secret
CORS_ORIGINS=http://127.0.0.1:5500
```

---

## Step 3 — Start Backend

```bash
python -m uvicorn main:app --reload --port 8000
```

FastAPI documentation will be available through the local API documentation interface.

---

## Step 4 — Seed Database

```bash
python seed.py
```

This imports the sample AgroTech products into the database.

---

## Step 5 — Start Frontend

Open a new terminal in the project root:

```bash
python -m http.server 5500
```

Then open the application in your browser using the local development server.

---

# 🎯 Project Objectives

The main objectives of AgroTech are:

### 🌾 Accessibility

Make agricultural resources easier for farmers to discover.

### 🚜 Equipment Availability

Improve access to agricultural machinery and equipment.

### 🤝 Service Connectivity

Connect farmers with agricultural service providers.

### 📦 Digital Management

Allow users to manage products, services, and orders digitally.

### 🔐 Secure Platform

Provide secure authentication and role-based administrative access.

### 📱 User-Friendly Experience

Create a simple and responsive platform suitable for different types of users.

---

# 🔮 Future Enhancements

AgroTech can be further enhanced with:

* 🤖 AI-based crop recommendations
* 🧠 AI-powered equipment recommendations
* 📍 Location-based machinery discovery
* 💳 Online payment gateway
* 🚚 Real-time delivery tracking
* 🌐 Multi-language support
* 📱 SMS and WhatsApp notifications
* 📈 Advanced analytics
* ☁️ Cloud deployment
* 🔄 CI/CD pipeline
* 🌦️ Weather-based farming recommendations

---

# 💡 Why AgroTech?

> **One platform. Multiple agricultural needs.**

AgroTech aims to bridge the gap between **farmers, agricultural equipment, products, and service providers** through technology.

Instead of managing different agricultural requirements through multiple offline channels, users can access essential services through a single digital platform.

---

# 👨‍💻 Developer

## Madhur Pratap Singh

**Computer Science & Engineering**

### Skills Used

```text
Python
FastAPI
HTML
CSS
JavaScript
Supabase
PostgreSQL
JWT
Git
GitHub
```

---

# ⭐ Project Highlights

```text
✓ Full-Stack Web Application
✓ REST API Architecture
✓ Secure Authentication
✓ Role-Based Admin Panel
✓ PostgreSQL Database
✓ Responsive Frontend
✓ Product Management
✓ Service Management
✓ Order Management
✓ Complaint Management
✓ Notification System
✓ Scalable Backend Architecture
```

---

# 🌱 Final Note

**AgroTech is more than an agricultural marketplace — it is a step toward building a digitally connected farming ecosystem.**

### 🚜 Technology + Agriculture = Smarter Farming

**Made with ❤️ for India's Farmers**

