import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Clothes Ecommerce API")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app/file.db")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_this_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    KHQR_GATEWAY_URL: str = os.getenv("KHQR_GATEWAY_URL", "https://khqr.cc/api/payment/request")
    KHQR_PROFILE_ID: str = os.getenv("KHQR_PROFILE_ID", "aEaG4uiBgUg0s69AaCxGbDoldlG7OZyz")
    KHQR_SECRET_KEY: str = os.getenv("KHQR_SECRET_KEY", "YOUR_SECRET_KEY")
    KHQR_PROFILE_KEY: str = os.getenv("KHQR_PROFILE_KEY", "YOUR_PROFILE_KEY")
    KHQR_VERIFY_URL: str = os.getenv(
        "KHQR_VERIFY_URL",
        "https://khqr.cc/api/aEaG4uiBgUg0s69AaCxGbDoldlG7OZyz/payment-gateway/v1/payments/check-trans",
    )

    SITE_SUCCESS_URL: str = os.getenv("SITE_SUCCESS_URL", "http://localhost:8000/api/payments/success")

    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")


settings = Settings()
