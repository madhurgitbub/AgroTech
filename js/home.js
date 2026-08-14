// ===== Home Page JS =====

document.addEventListener('DOMContentLoaded', () => {
  requireAuth();
  renderNavbar('home');
  setGreeting();
  loadUserName();
  loadStats();
  renderProducts();
});

function setGreeting() {
  const hour = new Date().getHours();
  const el = document.getElementById('greeting');
  if (!el) return;
  if (hour < 12) el.textContent = 'Good morning! 🌤';
  else if (hour < 17) el.textContent = 'Good afternoon! ☀️';
  else el.textContent = 'Good evening! 🌙';
}

function loadUserName() {
  const user = AgroData.getUser();
  const el = document.getElementById('userName');
  if (el) el.textContent = user.name.split(' ')[0] + '?';
}

function loadStats() {
  const purchases = AgroData.getPurchases();
  const services  = AgroData.getServices();

  const total  = purchases.length;
  const active = purchases.filter(p => p.status === 'pending').length;
  const spent  = purchases.reduce((sum, p) => sum + (p.price || 0), 0);

  document.getElementById('totalPurchases').textContent = total;
  document.getElementById('activePurchases').textContent = active;
  document.getElementById('totalSpend').textContent = formatPrice(spent);
  document.getElementById('myServices').textContent = services.length;
}

function renderProducts() {
  const grid = document.getElementById('productGrid');
  if (!grid) return;
  const featured = AgroData.products.slice(0, 8);
  grid.innerHTML = featured.map((p, i) => createProductCard(p, i)).join('');
}

function createProductCard(p, i = 0) {
  return `
    <div class="product-card animate-fade-up" style="animation-delay:${i * 0.05}s">
      <img class="product-card-img" src="${p.image}" alt="${p.name}"
           onerror="this.src='https://via.placeholder.com/300x160/e8f5e9/2e7d32?text=${encodeURIComponent(p.name)}'"
           onclick="viewDetail(${p.id})" style="cursor:pointer">
      <div class="product-card-body">
        <div class="product-card-cat">${getCategoryIcon(p.category)} ${p.category}</div>
        <div class="product-card-name" onclick="viewDetail(${p.id})" style="cursor:pointer">${p.name}</div>
        <div class="product-card-desc">${p.description}</div>
        <div class="product-card-meta">
          <div class="product-card-price">${formatPrice(p.price)} <span>/ ${p.unit}</span></div>
          <div class="product-card-rating">★ ${p.rating} <span style="color:#999">(${p.reviews})</span></div>
        </div>
        <div class="product-card-location">📍 ${p.location}</div>
        <div style="display:flex;gap:8px">
          <button class="btn btn-secondary btn-sm" style="flex:0 0 auto" onclick="viewDetail(${p.id})">👁 View</button>
          <button class="btn btn-primary btn-sm" style="flex:1" onclick="rentProduct(${p.id})">🛒 Rent</button>
        </div>
      </div>
    </div>
  `;
}

function viewDetail(id) {
  const product = AgroData.products.find(p => p.id === id);
  if (!product) return;
  sessionStorage.setItem('selected_product', JSON.stringify(product));
  window.location.href = 'product.html';
}

function rentProduct(id) {
  const product = AgroData.products.find(p => p.id === id);
  if (!product) return;
  sessionStorage.setItem('selected_product', JSON.stringify(product));
  window.location.href = 'buy.html';
}

function performSearch() {
  const q = document.getElementById('homeSearch').value.trim();
  if (q) window.location.href = `search.html?q=${encodeURIComponent(q)}`;
  else window.location.href = 'search.html';
}

document.getElementById('homeSearch')?.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') performSearch();
});
