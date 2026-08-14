// AgroTech API client. Change API_BASE when deploying the FastAPI backend.
const API_BASE = localStorage.getItem('agro_api_base') || 'http://127.0.0.1:8000/api';

async function apiRequest(path, options = {}) {
  const token = localStorage.getItem('agro_token');
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  let data = {};
  try { data = await res.json(); } catch (_) {}
  if (!res.ok) throw new Error(data.detail || data.message || `Request failed (${res.status})`);
  return data;
}

function setSession(data) {
  if (data.token) localStorage.setItem('agro_token', data.token);
  if (data.user) localStorage.setItem('agro_user', JSON.stringify(data.user));
}
function clearSession() {
  localStorage.removeItem('agro_token');
  localStorage.removeItem('agro_user');
}
async function apiLogin(username, password) {
  const data = await apiRequest('/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) });
  setSession(data); return data;
}
async function apiRegister(payload) {
  const data = await apiRequest('/auth/register', { method: 'POST', body: JSON.stringify(payload) });
  setSession(data); return data;
}
async function apiAdminLogin(username, password) {
  const data = await apiRequest('/admin/login', { method: 'POST', body: JSON.stringify({ username, password }) });
  setSession(data); localStorage.setItem('agro_admin_user', JSON.stringify(data.user)); return data;
}
async function apiAdminRegister(payload) {
  return apiRequest('/admin/register', { method: 'POST', body: JSON.stringify(payload) });
}
