# Clothes Ecommerce Backend

## Run PostgreSQL

```bash
docker compose up -d
```

## Setup backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py
```

Open:

```txt
http://127.0.0.1:8000/docs
```

PgAdmin:

```txt
http://127.0.0.1:5050
Email: admin@example.com
Password: admin123
```

PostgreSQL connection inside PgAdmin:

```txt
Host: postgres
Port: 5432
Database: clothes_ecommerce_db
Username: postgres
Password: postgres
```
