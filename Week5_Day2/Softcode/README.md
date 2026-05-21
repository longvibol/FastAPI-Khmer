# Clothes Ecommerce Full Stack Project

This project includes:

- Backend: FastAPI + PostgreSQL + SQLite option
- Frontend User: React.js CRA style + Tailwind CDN
- Frontend Admin: React.js CRA style + Tailwind CDN
- KHQR payment checkout integration
- Telegram bot alert integration
- Product image upload
- Admin dashboard

## 1. Start PostgreSQL

From the root folder:

```bash
docker compose up -d
```

## 2. Run Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py
```

Open backend docs:

```txt
http://127.0.0.1:8000/docs
```

## 3. Create Admin Account

Register the first user from Swagger docs or frontend_user.

The first registered user automatically becomes admin.

## 4. Run Frontend User

Open a new terminal:

```bash
cd frontend_user
npm install
copy .env.example .env
npm start
```

Open:

```txt
http://localhost:3000
```

## 5. Run Frontend Admin

Open another terminal:

```bash
cd frontend_admin
npm install
copy .env.example .env
set PORT=3001 && npm start
```

Open:

```txt
http://localhost:3001
```

## 6. PgAdmin

```txt
http://127.0.0.1:5050
Email: admin@example.com
Password: admin123
```

Add server:

```txt
Host: postgres
Port: 5432
Database: clothes_ecommerce_db
Username: postgres
Password: postgres
```

## 7. KHQR Payment Config

Edit backend `.env`:

```env
KHQR_SECRET_KEY=YOUR_SECRET_KEY
KHQR_PROFILE_KEY=YOUR_PROFILE_KEY
```

Do not mark payment as paid only because the user returned to the success page. The backend verifies the transaction with KHQR first.

## 8. Telegram Alert Config

Edit backend `.env`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Telegram alert is sent when:

- New order is created
- Payment is verified successfully
