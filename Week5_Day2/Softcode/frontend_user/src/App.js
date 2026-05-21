import React, { useEffect, useMemo, useState } from "react";
import { api, imageUrl, setToken, logout, getToken } from "./api";

function Header({ page, setPage, cartCount, user, setUser }) {
  const nav = ["home", "cart", "orders"];
  return (
    <header className="bg-white border-b sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <button onClick={() => setPage("home")} className="text-xl font-bold text-slate-900">Clothes Shop</button>
        <div className="flex items-center gap-2">
          {nav.map((n) => (
            <button key={n} onClick={() => setPage(n)} className={`px-3 py-2 rounded-xl capitalize ${page === n ? "bg-slate-900 text-white" : "hover:bg-slate-100"}`}>
              {n === "cart" ? `Cart (${cartCount})` : n}
            </button>
          ))}
          {user ? (
            <button onClick={() => { logout(); setUser(null); setPage("home"); }} className="px-3 py-2 rounded-xl bg-red-50 text-red-700">Logout</button>
          ) : (
            <button onClick={() => setPage("login")} className="px-3 py-2 rounded-xl bg-orange-600 text-white">Login</button>
          )}
        </div>
      </div>
    </header>
  );
}

function Login({ setPage, setUser }) {
  const [isRegister, setIsRegister] = useState(false);
  const [form, setForm] = useState({ full_name: "", gender: "Male", phone_number: "", email: "", password: "", confirm_password: "" });
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      if (isRegister) await api.register(form);
      const result = await api.login({ email: form.email, password: form.password });
      setToken(result.access_token);
      const me = await api.me();
      setUser(me);
      setPage("home");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 bg-white p-6 rounded-2xl shadow-sm border">
      <h1 className="text-2xl font-bold mb-4">{isRegister ? "Create Account" : "Login"}</h1>
      {error && <div className="mb-3 p-3 rounded-xl bg-red-50 text-red-700">{error}</div>}
      <form onSubmit={submit} className="space-y-3">
        {isRegister && <>
          <input className="w-full border p-3 rounded-xl" placeholder="Full name" value={form.full_name} onChange={e => setForm({...form, full_name:e.target.value})} />
          <select className="w-full border p-3 rounded-xl" value={form.gender} onChange={e => setForm({...form, gender:e.target.value})}>
            <option>Male</option><option>Female</option><option>Other</option>
          </select>
          <input className="w-full border p-3 rounded-xl" placeholder="Phone number" value={form.phone_number} onChange={e => setForm({...form, phone_number:e.target.value})} />
        </>}
        <input className="w-full border p-3 rounded-xl" placeholder="Email" type="email" value={form.email} onChange={e => setForm({...form, email:e.target.value})} />
        <input className="w-full border p-3 rounded-xl" placeholder="Password" type="password" value={form.password} onChange={e => setForm({...form, password:e.target.value})} />
        {isRegister && <input className="w-full border p-3 rounded-xl" placeholder="Confirm password" type="password" value={form.confirm_password} onChange={e => setForm({...form, confirm_password:e.target.value})} />}
        <button className="w-full bg-slate-900 text-white py-3 rounded-xl">{isRegister ? "Register" : "Login"}</button>
      </form>
      <button onClick={() => setIsRegister(!isRegister)} className="mt-4 text-orange-700">
        {isRegister ? "Already have account? Login" : "No account? Register"}
      </button>
    </div>
  );
}

function Home({ addToCart }) {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [category, setCategory] = useState("all");
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.products(), api.categories()]).then(([p, c]) => { setProducts(p); setCategories(c); }).finally(() => setLoading(false));
  }, []);

  const list = products.filter(p => {
    const matchCat = category === "all" || String(p.category_id) === category;
    const matchQuery = p.title.toLowerCase().includes(query.toLowerCase());
    return matchCat && matchQuery;
  });

  if (loading) return <div className="p-8 text-center">Loading products...</div>;

  return (
    <main className="max-w-6xl mx-auto px-4 py-8">
      <section className="bg-gradient-to-r from-orange-500 to-slate-900 text-white p-8 rounded-3xl mb-8">
        <h1 className="text-4xl font-bold mb-2">Shop Clothes Online</h1>
        <p className="opacity-90">Pay easily with KHQR using any Cambodian bank app.</p>
      </section>
      <div className="flex flex-col md:flex-row gap-3 mb-6">
        <input className="border p-3 rounded-xl flex-1" placeholder="Search product" value={query} onChange={e => setQuery(e.target.value)} />
        <select className="border p-3 rounded-xl" value={category} onChange={e => setCategory(e.target.value)}>
          <option value="all">All Categories</option>
          {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {list.map(product => <ProductCard key={product.id} product={product} addToCart={addToCart} />)}
      </div>
    </main>
  );
}

function ProductCard({ product, addToCart }) {
  const price = product.discount_price || product.original_price;
  const [size, setSize] = useState((product.sizes || "").split(",").filter(Boolean)[0] || "");
  const [color, setColor] = useState((product.colors || "").split(",").filter(Boolean)[0] || "");
  return (
    <div className="bg-white rounded-2xl shadow-sm border overflow-hidden flex flex-col">
      <img src={imageUrl(product.main_image)} alt={product.title} className="h-52 w-full object-cover" />
      <div className="p-4 flex-1 flex flex-col">
        <h3 className="font-bold text-lg line-clamp-2">{product.title}</h3>
        <div className="my-2 flex items-center gap-2">
          <span className="font-bold text-orange-700">${price.toFixed(2)}</span>
          {product.discount_price && <span className="line-through text-slate-400 text-sm">${product.original_price.toFixed(2)}</span>}
        </div>
        <div className="space-y-2 text-sm mb-3">
          {product.sizes && <select className="w-full border rounded-lg p-2" value={size} onChange={e => setSize(e.target.value)}>{product.sizes.split(",").map(s => <option key={s}>{s}</option>)}</select>}
          {product.colors && <select className="w-full border rounded-lg p-2" value={color} onChange={e => setColor(e.target.value)}>{product.colors.split(",").map(c => <option key={c}>{c}</option>)}</select>}
        </div>
        <button onClick={() => addToCart({ product_id: product.id, product_title: product.title, price, size, color, quantity: 1, main_image: product.main_image })} className="mt-auto bg-slate-900 text-white py-2 rounded-xl">Add to Cart</button>
      </div>
    </div>
  );
}

function Cart({ cart, setCart, setPage, user }) {
  const [error, setError] = useState("");
  const total = useMemo(() => cart.reduce((s, i) => s + i.price * i.quantity, 0), [cart]);

  const changeQty = (idx, q) => setCart(cart.map((item, i) => i === idx ? { ...item, quantity: Math.max(1, q) } : item));
  const remove = (idx) => setCart(cart.filter((_, i) => i !== idx));

  const checkout = async () => {
    if (!user) { setPage("login"); return; }
    setError("");
    try {
      const items = cart.map(({ product_id, size, color, quantity }) => ({ product_id, size, color, quantity }));
      const order = await api.createOrder(items);
      const payment = await api.checkout(order.id);
      window.location.href = payment.checkout_url;
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <main className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-5">Shopping Cart</h1>
      {error && <div className="mb-3 p-3 bg-red-50 text-red-700 rounded-xl">{error}</div>}
      {cart.length === 0 ? <p>Your cart is empty.</p> : <div className="space-y-3">
        {cart.map((item, idx) => (
          <div key={idx} className="bg-white border rounded-2xl p-4 flex gap-4 items-center">
            <img src={imageUrl(item.main_image)} alt="" className="w-24 h-24 object-cover rounded-xl" />
            <div className="flex-1">
              <h3 className="font-bold">{item.product_title}</h3>
              <p className="text-sm text-slate-500">Size: {item.size || "-"} | Color: {item.color || "-"}</p>
              <p className="font-semibold">${item.price.toFixed(2)}</p>
            </div>
            <input type="number" min="1" className="border rounded-lg p-2 w-20" value={item.quantity} onChange={e => changeQty(idx, Number(e.target.value))} />
            <button onClick={() => remove(idx)} className="text-red-600">Remove</button>
          </div>
        ))}
        <div className="bg-white border rounded-2xl p-5 flex justify-between items-center">
          <div className="text-xl font-bold">Total: ${total.toFixed(2)}</div>
          <button onClick={checkout} className="bg-orange-600 text-white px-6 py-3 rounded-xl">Checkout with KHQR</button>
        </div>
      </div>}
    </main>
  );
}

function Orders() {
  const [orders, setOrders] = useState([]);
  const [msg, setMsg] = useState("");
  useEffect(() => { if (getToken()) api.myOrders().then(setOrders).catch(e => setMsg(e.message)); }, []);
  const verify = async (tx) => {
    try { const r = await api.verify(tx); setMsg(r.is_paid ? "Payment verified successfully." : `Payment not paid yet: ${r.status}`); setOrders(await api.myOrders()); }
    catch(e) { setMsg(e.message); }
  };
  return <main className="max-w-5xl mx-auto px-4 py-8">
    <h1 className="text-3xl font-bold mb-5">My Orders</h1>
    {msg && <div className="mb-3 p-3 bg-blue-50 text-blue-700 rounded-xl">{msg}</div>}
    <div className="space-y-3">{orders.map(o => <div key={o.id} className="bg-white border rounded-2xl p-4">
      <div className="flex justify-between"><b>{o.transaction_id}</b><span>${o.total_amount.toFixed(2)}</span></div>
      <p className="text-sm text-slate-500">Order: {o.status} | Payment: {o.payment_status}</p>
      <button onClick={() => verify(o.transaction_id)} className="mt-2 px-3 py-2 rounded-xl bg-slate-900 text-white">Verify Payment</button>
    </div>)}</div>
  </main>;
}

function App() {
  const [page, setPage] = useState("home");
  const [cart, setCart] = useState(() => JSON.parse(localStorage.getItem("cart") || "[]"));
  const [user, setUser] = useState(null);

  useEffect(() => { localStorage.setItem("cart", JSON.stringify(cart)); }, [cart]);
  useEffect(() => { if (getToken()) api.me().then(setUser).catch(() => logout()); }, []);

  const addToCart = (item) => {
    setCart(prev => [...prev, item]);
    setPage("cart");
  };

  return <>
    <Header page={page} setPage={setPage} cartCount={cart.length} user={user} setUser={setUser} />
    {page === "home" && <Home addToCart={addToCart} />}
    {page === "login" && <Login setPage={setPage} setUser={setUser} />}
    {page === "cart" && <Cart cart={cart} setCart={setCart} setPage={setPage} user={user} />}
    {page === "orders" && <Orders />}
  </>;
}

export default App;
