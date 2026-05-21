const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export const getToken = () => localStorage.getItem("admin_token");
export const setToken = (token) => localStorage.setItem("admin_token", token);
export const logout = () => localStorage.removeItem("admin_token");

export function imageUrl(path) {
  if (!path) return "https://placehold.co/600x400?text=No+Image";
  if (path.startsWith("http")) return path;
  return `${API_URL}${path}`;
}

async function request(path, options = {}) {
  const headers = options.headers || {};
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  if (!(options.body instanceof FormData)) headers["Content-Type"] = "application/json";
  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  const data = await res.json().catch(() => null);
  if (!res.ok) throw new Error(data?.detail || "Request failed");
  return data;
}

export const api = {
  login: (data) => request("/api/auth/login", { method: "POST", body: JSON.stringify(data) }),
  me: () => request("/api/auth/me"),
  stats: () => request("/api/admin/stats"),
  users: () => request("/api/users/"),
  categories: () => request("/api/categories/"),
  createCategory: (data) => request("/api/categories/", { method: "POST", body: JSON.stringify(data) }),
  deleteCategory: (id) => request(`/api/categories/${id}`, { method: "DELETE" }),
  products: () => request("/api/products/"),
  createProduct: (formData) => request("/api/products/", { method: "POST", body: formData, headers: {} }),
  deleteProduct: (id) => request(`/api/products/${id}`, { method: "DELETE" }),
  orders: () => request("/api/orders/"),
  updateOrderStatus: (id, status) => request(`/api/orders/${id}/status`, { method: "PUT", body: JSON.stringify({ status }) }),
  backup: () => `${API_URL}/api/backup/download`,
};
