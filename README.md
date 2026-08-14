# 🌱 AgroTECH — Smart Agricultural Equipment Rental Platform

A complete multi-page web application for farmers to rent machinery, buy seeds/fertilizers, and connect with agricultural service providers.

---

## 📁 Project Structure

```
agrotech/
├── index.html              ← Landing page (public)
├── 404.html                ← Custom 404 page
├── data/
│   └── data.json           ← Product, category & seed data
├── css/
│   ├── global.css          ← Design system, shared components
│   ├── index.css           ← Landing page styles
│   └── home.css            ← Home dashboard + product card styles
├── js/
│   ├── global.js           ← Data store (AgroData), utilities, navbar
│   └── home.js             ← Home page logic
└── pages/
    ├── login.html          ← Login with validation
    ├── register.html       ← Multi-step registration
    ├── home.html           ← Main dashboard (protected)
    ├── search.html         ← Browse & filter all products
    ├── product.html        ← Product detail with tabs & reviews
    ├── buy.html            ← Order + 4-method payment
    ├── addService.html     ← List a new service
    ├── my_services.html    ← CRUD manage own listings
    ├── my_purchase.html    ← Order history & status
    ├── myaccount.html      ← Profile view & edit
    ├── wishlist.html       ← Saved products
    ├── notifications.html  ← Activity notifications
    └── help.html           ← FAQ + support form
```

---

## 🚀 How to Run

### Option 1 — Open directly in browser
Just double-click `index.html`. All pages work from the file system.

### Option 2 — Local dev server (recommended, avoids CORS quirks)
```bash
# Python 3
python3 -m http.server 3000

# Node.js (npx)
npx serve .

# VS Code — install "Live Server" extension and click "Go Live"
```
Then open: `http://localhost:3000`

---

## 🔑 Demo Login

Any username + password (min 4 chars) will log you in.  
Example: `farmer` / `1234`

---

## 💳 Payment Methods Supported

| Method | Details |
|--------|---------|
| Cash on Delivery | No upfront payment |
| Card (Debit/Credit) | 16-digit card with auto-formatting |
| UPI / GPay / PhonePe | Enter UPI ID (e.g. `name@upi`) |
| Wallet | One-click wallet payment |

---

## 📦 Features Built

- ✅ Landing page with hero, features, about, CTA
- ✅ Register with validation & step indicator
- ✅ Login with password toggle & enter-key support
- ✅ Home dashboard with greeting, stats, product grid
- ✅ Search with live filter, category tabs, sort
- ✅ Product detail — image, tabs (desc/specs/reviews), related, star rating
- ✅ Buy/Rent page with 4 payment methods & order confirmation modal
- ✅ Add Service with image preview, char counter, validations
- ✅ My Services — toggle active/inactive, edit modal, delete confirm
- ✅ My Purchases — history, status badges, filter tabs
- ✅ My Account — profile view/edit with inline toggle
- ✅ Wishlist — save/remove products
- ✅ Notifications — mark read/unread, filter by type
- ✅ Help — accordion FAQ (Hindi + English), support form
- ✅ Mobile-responsive navbar with hamburger menu
- ✅ Toast notifications system-wide
- ✅ LocalStorage persistence for all user data
- ✅ Auth guard on all protected pages
- ✅ Custom 404 page

---

## 🎨 Tech Stack

| Layer | Tech |
|-------|------|
| Markup | Semantic HTML5 |
| Styling | CSS3 with custom design system (CSS variables) |
| Fonts | Sora (headings) + DM Sans (body) via Google Fonts |
| Logic | Vanilla JavaScript (ES6+) |
| Data | JSON + localStorage |
| Icons | Emoji-based (no external dependency) |

---

## 🛠 Extending to a Real Backend

The `AgroData` object in `js/global.js` is the data layer.  
To connect a real backend (Node/Django/FastAPI):

1. Replace `AgroData.products` with an `async` fetch to your API
2. Replace `localStorage` calls with API POST/GET requests
3. Add JWT token management in `AgroData.login()` / `AgroData.isLoggedIn()`

---

*Built with 💚 for India's Farmers — AgroTECH 2025*
"# AgroTech" 
