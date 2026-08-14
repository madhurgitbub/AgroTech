// ===== AgroTech Global JavaScript =====

// ---- Data Store (simulates JSON backend) ----
const AgroData = {
  // Embedded data since we can't fetch local JSON in file:// mode
  products: [
    { id: 1, name: "Mahindra Tractor", category: "machinery", price: 800, unit: "per acre", description: "Powerful 45HP tractor suitable for ploughing, tilling, and heavy-duty farming tasks. GPS-enabled for precision agriculture.", image: "https://5.imimg.com/data5/SELLER/Default/2021/6/CX/WL/RI/30912792/mahindra-tractor-yuvraj-bumper-1000x1000.jpg", rating: 4.5, reviews: 128, available: true, location: "Indore, MP" },
    { id: 2, name: "John Deere Tractor", category: "machinery", price: 1000, unit: "per acre", description: "High-efficiency John Deere with advanced hydraulics. Perfect for large-scale farming operations.", image: "https://cpimg.tistatic.com/10029058/b/4/John-deere-Tractors..jpg", rating: 4.8, reviews: 95, available: true, location: "Bhopal, MP" },
    { id: 3, name: "Combine Harvester", category: "machinery", price: 1200, unit: "per acre", description: "Modern combine harvester for wheat, rice, and soybean. Cuts harvesting time by 70%.", image: "https://5.imimg.com/data5/WC/IE/YH/ANDROID-86040604/prod-20200810-2031297210080910753376724-jpg-1000x1000.jpg", rating: 4.6, reviews: 72, available: true, location: "Ujjain, MP" },
    { id: 4, name: "Rotavator", category: "machinery", price: 500, unit: "per acre", description: "Heavy-duty rotavator for soil preparation. Breaks clods and prepares perfect seedbed.", image: "https://www.fieldking.com/blogs/wp-content/uploads/2024/09/Ploughing.jpg", rating: 4.3, reviews: 64, available: true, location: "Gwalior, MP" },
    { id: 5, name: "Drip Irrigation Kit", category: "irrigation", price: 3500, unit: "per kit", description: "Complete drip irrigation setup for 1 acre. Saves 60% water and increases yield.", image: "https://5.imimg.com/data5/SELLER/Default/2022/10/BC/MY/LI/21395960/drip-irrigation-system-1000x1000.jpg", rating: 4.7, reviews: 89, available: true, location: "Indore, MP" },
    { id: 6, name: "DAP Fertilizer (50kg)", category: "fertilizer", price: 1350, unit: "per bag", description: "High-quality DAP fertilizer for improved root development and yield.", image: "https://5.imimg.com/data5/SELLER/Default/2022/5/NJ/VT/MB/26553143/dap-fertilizer-500x500.jpg", rating: 4.4, reviews: 201, available: true, location: "Bhopal, MP" },
    { id: 7, name: "Wheat Seeds (Premium)", category: "seeds", price: 450, unit: "per kg", description: "High-yield HYV wheat seeds. Disease resistant, drought tolerant. Yield: 45-55 q/ha.", image: "https://5.imimg.com/data5/SELLER/Default/2021/9/ZG/OS/PB/3131427/wheat-seeds-500x500.jpg", rating: 4.6, reviews: 156, available: true, location: "Sehore, MP" },
    { id: 8, name: "Mini Truck Transport", category: "transport", price: 2500, unit: "per trip", description: "5-ton capacity mini truck for crop transport. Available 24/7 within 100km radius.", image: "https://5.imimg.com/data5/SELLER/Default/2022/3/QF/XN/XJ/149399990/mini-truck-500x500.jpg", rating: 4.2, reviews: 43, available: true, location: "Indore, MP" }
  ],
  categories: ["All", "machinery", "irrigation", "fertilizer", "seeds", "transport"],
  currentUser: {
    id: 1, name: "Madhur Pratap Singh",
    email: "madhurpratapsingh2005@gmail.com",
    phone: "8127059423",
    location: "Indore, MP",
    role: "farmer"
  },

  // Local storage helpers
  getPurchases() {
    return JSON.parse(localStorage.getItem('agro_purchases') || '[]');
  },
  savePurchase(purchase) {
    const purchases = this.getPurchases();
    purchase.id = Date.now();
    purchases.unshift(purchase);
    localStorage.setItem('agro_purchases', JSON.stringify(purchases));
    return purchase;
  },
  getServices() {
    return JSON.parse(localStorage.getItem('agro_services') || '[]');
  },
  saveService(service) {
    const services = this.getServices();
    service.id = Date.now();
    services.unshift(service);
    localStorage.setItem('agro_services', JSON.stringify(services));
    return service;
  },
  getUser() {
    return JSON.parse(localStorage.getItem('agro_user') || JSON.stringify(this.currentUser));
  },
  saveUser(user) {
    localStorage.setItem('agro_user', JSON.stringify(user));
  },
  isLoggedIn() {
    return !!localStorage.getItem('agro_token');
  },
  login(username, password) {
    return !!localStorage.getItem('agro_token');
  },
  logout() {
    if (typeof clearSession === 'function') clearSession(); else localStorage.removeItem('agro_token');
  }
};

// ---- Utility Functions ----

function showToast(message, type = 'success', duration = 3000) {
  let toast = document.getElementById('global-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'global-toast';
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${icons[type] || '💬'}</span> <span>${message}</span>`;
  toast.classList.add('show');
  clearTimeout(toast._timeout);
  toast._timeout = setTimeout(() => toast.classList.remove('show'), duration);
}

function formatPrice(price) {
  return '₹' + price.toLocaleString('en-IN');
}

function formatDate(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

function renderStars(rating) {
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5 ? 1 : 0;
  const empty = 5 - full - half;
  return '★'.repeat(full) + (half ? '½' : '') + '☆'.repeat(empty);
}

function getCategoryIcon(cat) {
  const icons = { machinery: '🚜', irrigation: '💧', fertilizer: '🌿', seeds: '🌱', transport: '🚛', other: '📦' };
  return icons[cat] || '📦';
}

function debounce(fn, delay = 300) {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), delay); };
}

// Redirect if not logged in (call on protected pages)
function requireAuth() {
  if (!AgroData.isLoggedIn()) {
    window.location.href = '../pages/login.html';
    return false;
  }
  return true;
}

// Render navbar dynamically
function renderNavbar(activePage = '') {
  const user = AgroData.getUser();
  const nav = document.getElementById('navbar');
  if (!nav) return;
  nav.innerHTML = `
    <a href="../pages/home.html" class="navbar-logo">
      <div class="logo-icon">🌱</div>
      Agro<span>TECH</span>
    </a>
    <ul class="navbar-links" id="navLinks">
      <li><a href="../pages/home.html" class="${activePage==='home'?'active':''}">🏠 Home</a></li>
      <li><a href="../pages/search.html" class="${activePage==='search'?'active':''}">🔍 Search</a></li>
      <li><a href="../pages/notifications.html" class="${activePage==='notif'?'active':''}">🔔 Alerts</a></li>
      <li><a href="../pages/wishlist.html" class="${activePage==='wishlist'?'active':''}">🤍 Wishlist</a></li>
      <li><a href="../pages/my_services.html" class="${activePage==='services'?'active':''}">📋 My Services</a></li>
      <li><a href="../pages/my_purchase.html" class="${activePage==='purchases'?'active':''}">📦 Purchases</a></li>
      <li><a href="../pages/myaccount.html" class="${activePage==='account'?'active':''}">👤 ${user.name.split(' ')[0]}</a></li>
      <li><a href="../pages/help.html" class="${activePage==='help'?'active':''}">❓ Help</a></li>
      <li><button class="btn-logout" onclick="handleLogout()">🚪 Logout</button></li>
    </ul>
    <button class="mobile-menu-btn" onclick="toggleMobileMenu()">☰</button>
  `;
}

function handleLogout() {
  if (confirm('Are you sure you want to logout?')) {
    AgroData.logout();
    showToast('Logged out successfully', 'info');
    setTimeout(() => { window.location.href = '../index.html'; }, 1000);
  }
}

function toggleMobileMenu() {
  const links = document.querySelector('.navbar-links');
  if (links) links.style.display = links.style.display === 'flex' ? 'none' : 'flex';
}

// ===== Mobile Menu Toggle (updated) =====
function toggleMobileMenu() {
  const links = document.querySelector('.navbar-links');
  if (links) links.classList.toggle('open');
}

// Close mobile menu on outside click
document.addEventListener('click', (e) => {
  if (!e.target.closest('.navbar')) {
    document.querySelector('.navbar-links')?.classList.remove('open');
  }
});
