# Clothes Ecommerce Backend — FastAPI + SQLite

This backend supports:

- User register/login
- Product CRUD with main image and multiple sub images
- Category CRUD with parent category support
- Order creation and order detail
- KHQR checkout URL generation
- KHQR transaction verification
- Telegram bot alert for new orders and successful payments
- SQLite backup download as `file.db`

---

## 1. Open in PyCharm

1. Extract the ZIP file.
2. Open PyCharm.
3. Click **Open**.
4. Select the folder: `clothes_ecommerce_fastapi_backend`.
5. Open Terminal inside PyCharm.

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Packages

```bash
pip install -r requirements.txt
```

---

## 4. Create `.env`

Copy `.env.example` and rename it to `.env`.

Then update your real values:

```env
KHQR_SECRET_KEY=YOUR_REAL_SECRET_KEY
KHQR_PROFILE_KEY=YOUR_REAL_PROFILE_KEY
TELEGRAM_BOT_TOKEN=YOUR_REAL_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_REAL_CHAT_ID
```

---

## 5. Run Backend

```bash
python run.py
```

or:

```bash
uvicorn app.main:app --reload
```

---

## 6. Open API Docs

Open this URL in browser:

```txt
http://localhost:8000/docs
```

---

## 7. Important API URLs

```txt
POST   /api/auth/register
POST   /api/auth/login
GET    /api/users/me

POST   /api/categories/
GET    /api/categories/

POST   /api/products/
GET    /api/products/
GET    /api/products/{product_id}
PUT    /api/products/{product_id}
DELETE /api/products/{product_id}

POST   /api/orders/
GET    /api/orders/my-orders
GET    /api/orders/{order_id}

GET    /api/payments/checkout/{order_id}
GET    /api/payments/success
POST   /api/payments/verify/{transaction_id}

GET    /api/backup/download
```

---

## 8. First Test Flow

1. Register user.
2. Login user and copy the access token.
3. Click **Authorize** in Swagger.
4. Paste token like this:

```txt
Bearer YOUR_ACCESS_TOKEN
```

5. Create category.
6. Create product with image upload.
7. Create order.
8. Generate KHQR checkout URL.
9. Verify payment transaction.

---

## 9. Image Upload Paths

Uploaded images are saved here:

```txt
app/uploads/products/main/
app/uploads/products/sub/
```

Images can be viewed from browser using:

```txt
http://localhost:8000/uploads/products/main/filename.jpg
http://localhost:8000/uploads/products/sub/filename.jpg
```

---

## 10. SQLite Database

Database file:

```txt
app/file.db
```

Backup API:

```txt
http://localhost:8000/api/backup/download
```
