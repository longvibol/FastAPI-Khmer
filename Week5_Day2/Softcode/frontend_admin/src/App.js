import React, { useEffect, useState } from "react";
import { api, setToken, logout, getToken, imageUrl } from "./api";

function Login({ setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await api.login({ email, password });
      if (res.role !== "admin") throw new Error("This account is not admin. First registered user becomes admin.");
      setToken(res.access_token);
      setUser(await api.me());
    } catch (err) { setError(err.message); }
  };
  return <div className="min-h-screen flex items-center justify-center bg-slate-100 p-4">
    <form onSubmit={submit} className="bg-white p-6 rounded-2xl shadow-sm border w-full max-w-md">
      <h1 className="text-2xl font-bold mb-4">Admin Login</h1>
      {error && <div className="mb-3 p-3 bg-red-50 text-red-700 rounded-xl">{error}</div>}
      <input className="w-full border p-3 rounded-xl mb-3" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input className="w-full border p-3 rounded-xl mb-3" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button className="w-full bg-slate-900 text-white py-3 rounded-xl">Login</button>
      <p className="text-sm text-slate-500 mt-3">Note: the first registered backend user automatically becomes admin.</p>
    </form>
  </div>;
}

function Layout({ page, setPage, user, setUser, children }) {
  const tabs = ["dashboard", "products", "categories", "orders", "users"];
  return <div className="min-h-screen flex bg-slate-100">
    <aside className="w-64 bg-slate-950 text-white p-5 hidden md:block">
      <h1 className="text-xl font-bold mb-6">Admin Panel</h1>
      <div className="space-y-2">{tabs.map(t => <button key={t} onClick={() => setPage(t)} className={`w-full text-left px-4 py-3 rounded-xl capitalize ${page===t ? "bg-orange-600" : "hover:bg-slate-800"}`}>{t}</button>)}</div>
    </aside>
    <main className="flex-1">
      <header className="bg-white border-b p-4 flex justify-between items-center">
        <div><b>{user?.full_name}</b><p className="text-sm text-slate-500">Administrator</p></div>
        <button onClick={() => { logout(); setUser(null); }} className="px-4 py-2 bg-red-50 text-red-700 rounded-xl">Logout</button>
      </header>
      <div className="p-5 md:hidden flex gap-2 overflow-x-auto">{tabs.map(t => <button key={t} onClick={() => setPage(t)} className="px-3 py-2 bg-white rounded-xl border capitalize">{t}</button>)}</div>
      <div className="p-5">{children}</div>
    </main>
  </div>;
}

function Dashboard() {
  const [stats, setStats] = useState(null);
  useEffect(() => { api.stats().then(setStats); }, []);
  if (!stats) return <p>Loading...</p>;
  const cards = [
    ["Users", stats.users], ["Products", stats.products], ["Categories", stats.categories],
    ["Orders", stats.orders], ["Paid Orders", stats.paid_orders], ["Total Sales", `$${stats.total_sales}`]
  ];
  return <div>
    <h1 className="text-3xl font-bold mb-5">Dashboard</h1>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">{cards.map(([label, value]) => <div key={label} className="bg-white rounded-2xl p-5 border shadow-sm"><p className="text-slate-500">{label}</p><h2 className="text-3xl font-bold mt-2">{value}</h2></div>)}</div>
  </div>;
}

function Categories() {
  const [categories, setCategories] = useState([]);
  const [name, setName] = useState("");
  const [parentId, setParentId] = useState("");
  const [msg, setMsg] = useState("");
  const load = () => api.categories().then(setCategories);
  useEffect(() => { load(); }, []);
  const submit = async (e) => { e.preventDefault(); try { await api.createCategory({ name, parent_id: parentId ? Number(parentId) : null }); setName(""); setParentId(""); setMsg("Category created"); load(); } catch(e){ setMsg(e.message); }};
  return <div>
    <h1 className="text-3xl font-bold mb-5">Categories</h1>
    {msg && <div className="mb-3 p-3 rounded-xl bg-blue-50 text-blue-700">{msg}</div>}
    <form onSubmit={submit} className="bg-white p-4 rounded-2xl border mb-5 grid md:grid-cols-3 gap-3">
      <input className="border p-3 rounded-xl" placeholder="Category name" value={name} onChange={e => setName(e.target.value)} />
      <select className="border p-3 rounded-xl" value={parentId} onChange={e => setParentId(e.target.value)}><option value="">No parent</option>{categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}</select>
      <button className="bg-slate-900 text-white rounded-xl">Add Category</button>
    </form>
    <div className="bg-white rounded-2xl border overflow-hidden"><table className="w-full text-left"><thead className="bg-slate-50"><tr><th className="p-3">ID</th><th>Name</th><th>Parent ID</th><th></th></tr></thead><tbody>{categories.map(c => <tr key={c.id} className="border-t"><td className="p-3">{c.id}</td><td>{c.name}</td><td>{c.parent_id || "-"}</td><td><button onClick={async()=>{await api.deleteCategory(c.id); load();}} className="text-red-600">Delete</button></td></tr>)}</tbody></table></div>
  </div>;
}

function Products() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [msg, setMsg] = useState("");
  const [form, setForm] = useState({ title: "", original_price: "", discount_price: "", category_id: "", colors: "Black,White", sizes: "S,M,L,XL", description: "" });
  const [mainImage, setMainImage] = useState(null);
  const [subImages, setSubImages] = useState([]);
  const load = async () => { setProducts(await api.products()); setCategories(await api.categories()); };
  useEffect(() => { load(); }, []);
  const submit = async (e) => {
    e.preventDefault(); setMsg("");
    try {
      const fd = new FormData(); Object.entries(form).forEach(([k,v]) => { if (v !== "") fd.append(k,v); });
      if (mainImage) fd.append("main_image", mainImage);
      Array.from(subImages).forEach(img => fd.append("sub_images", img));
      await api.createProduct(fd); setMsg("Product created"); setForm({ title: "", original_price: "", discount_price: "", category_id: "", colors: "Black,White", sizes: "S,M,L,XL", description: "" }); load();
    } catch (e) { setMsg(e.message); }
  };
  return <div>
    <h1 className="text-3xl font-bold mb-5">Products</h1>
    {msg && <div className="mb-3 p-3 rounded-xl bg-blue-50 text-blue-700">{msg}</div>}
    <form onSubmit={submit} className="bg-white p-4 rounded-2xl border mb-5 grid md:grid-cols-2 gap-3">
      <input className="border p-3 rounded-xl" placeholder="Product title" value={form.title} onChange={e=>setForm({...form,title:e.target.value})} />
      <select className="border p-3 rounded-xl" value={form.category_id} onChange={e=>setForm({...form,category_id:e.target.value})}><option value="">Select category</option>{categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}</select>
      <input className="border p-3 rounded-xl" placeholder="Original price" type="number" step="0.01" value={form.original_price} onChange={e=>setForm({...form,original_price:e.target.value})} />
      <input className="border p-3 rounded-xl" placeholder="Discount price" type="number" step="0.01" value={form.discount_price} onChange={e=>setForm({...form,discount_price:e.target.value})} />
      <input className="border p-3 rounded-xl" placeholder="Colors comma separated" value={form.colors} onChange={e=>setForm({...form,colors:e.target.value})} />
      <input className="border p-3 rounded-xl" placeholder="Sizes comma separated" value={form.sizes} onChange={e=>setForm({...form,sizes:e.target.value})} />
      <textarea className="border p-3 rounded-xl md:col-span-2" placeholder="Description" value={form.description} onChange={e=>setForm({...form,description:e.target.value})}></textarea>
      <div><label className="text-sm font-semibold">Main Image</label><input className="block mt-2" type="file" onChange={e=>setMainImage(e.target.files[0])} /></div>
      <div><label className="text-sm font-semibold">Sub Images</label><input className="block mt-2" type="file" multiple onChange={e=>setSubImages(e.target.files)} /></div>
      <button className="bg-slate-900 text-white py-3 rounded-xl md:col-span-2">Create Product</button>
    </form>
    <div className="grid md:grid-cols-3 gap-4">{products.map(p => <div key={p.id} className="bg-white border rounded-2xl p-4"><img src={imageUrl(p.main_image)} alt="" className="w-full h-40 object-cover rounded-xl mb-3"/><h3 className="font-bold">{p.title}</h3><p className="text-orange-700 font-semibold">${(p.discount_price || p.original_price).toFixed(2)}</p><button onClick={async()=>{await api.deleteProduct(p.id); load();}} className="mt-2 text-red-600">Delete</button></div>)}</div>
  </div>;
}

function Orders() {
  const [orders, setOrders] = useState([]);
  const load = () => api.orders().then(setOrders);
  useEffect(() => { load(); }, []);
  const statuses = ["PENDING", "PROCESSING", "PAID", "SHIPPED", "COMPLETED", "CANCELLED", "FAILED"];
  return <div>
    <h1 className="text-3xl font-bold mb-5">Orders</h1>
    <div className="space-y-3">{orders.map(o => <div key={o.id} className="bg-white border rounded-2xl p-4">
      <div className="flex justify-between gap-3"><b>{o.transaction_id}</b><span className="font-bold">${o.total_amount.toFixed(2)}</span></div>
      <p className="text-sm text-slate-500">User ID: {o.user_id} | Payment: {o.payment_status}</p>
      <div className="mt-3 flex gap-3 items-center"><select className="border rounded-xl p-2" value={o.status} onChange={async e => { await api.updateOrderStatus(o.id, e.target.value); load(); }}>{statuses.map(s => <option key={s}>{s}</option>)}</select></div>
      <div className="mt-3 text-sm">{o.items.map(i => <div key={i.id}>• {i.product_title} / {i.size || "-"} / {i.color || "-"} x {i.quantity}</div>)}</div>
    </div>)}</div>
  </div>;
}

function Users() {
  const [users, setUsers] = useState([]);
  useEffect(() => { api.users().then(setUsers); }, []);
  return <div><h1 className="text-3xl font-bold mb-5">Users</h1><div className="bg-white rounded-2xl border overflow-hidden"><table className="w-full text-left"><thead className="bg-slate-50"><tr><th className="p-3">ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Role</th></tr></thead><tbody>{users.map(u => <tr key={u.id} className="border-t"><td className="p-3">{u.id}</td><td>{u.full_name}</td><td>{u.email}</td><td>{u.phone_number}</td><td>{u.role}</td></tr>)}</tbody></table></div></div>;
}

function App() {
  const [user, setUser] = useState(null);
  const [page, setPage] = useState("dashboard");
  useEffect(() => { if (getToken()) api.me().then(u => { if (u.role === "admin") setUser(u); else logout(); }).catch(() => logout()); }, []);
  if (!user) return <Login setUser={setUser} />;
  return <Layout page={page} setPage={setPage} user={user} setUser={setUser}>
    {page === "dashboard" && <Dashboard />}
    {page === "categories" && <Categories />}
    {page === "products" && <Products />}
    {page === "orders" && <Orders />}
    {page === "users" && <Users />}
  </Layout>;
}

export default App;
