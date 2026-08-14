# AgroTech — Run Guide

## Backend
1. Open `backend/.env.example` and create `backend/.env` with your Supabase URL, service-role key and JWT secret.
2. Run `backend/run_backend.bat` on Windows, or use the commands in `backend/README.md`.
3. Run `python backend/seed.py` once to import the sample products.

## Frontend
In the project root run:

```bash
python -m http.server 5500
```

Then open `http://127.0.0.1:5500/`.

## What is connected to the backend
- Farmer registration/login
- Admin registration/login
- JWT session
- User profile/session
- Product API
- Service create/list/update/delete
- Orders/purchases
- Admin dashboard
- Admin user management
- Admin listing/service approval
- Admin order status
- Admin payments view
- Admin complaints view/status
- Admin notifications

The browser never receives the Supabase service-role key.
