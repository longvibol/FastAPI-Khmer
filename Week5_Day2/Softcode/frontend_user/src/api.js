const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export const getToken = () => localStorage.getItem("token");
export const setToken = (token) => localStorage.setItem("token", token);
export const logout = () => localStorage.removeItem("token");

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
  if (!res.ok) {
  if (Array.isArray(data?.detail)) {
    const message = data.detail
      .map((err) => `${err.loc?.[err.loc.length - 1]}: ${err.msg}`)
      .join(" | ");
    throw new Error(message);
  }

  throw new Error(data?.detail || "Request failed");
}
  return data;
}

export const api = {
  register: (data) => request("/api/auth/register", { method: "POST", body: JSON.stringify(data) }),
  login: (data) => request("/api/auth/login", { method: "POST", body: JSON.stringify(data) }),
  me: () => request("/api/auth/me"),
  categories: () => request("/api/categories/"),
  products: () => request("/api/products/"),
  product: (id) => request(`/api/products/${id}`),
  createOrder: (items) => request("/api/orders/", { method: "POST", body: JSON.stringify({ items }) }),
  myOrders: () => request("/api/orders/my-orders"),
  checkout: (orderId) => request(`/api/payments/checkout/${orderId}`),
  verify: (transactionId) => request(`/api/payments/verify/${transactionId}`, { method: "POST" }),
};
