from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Clothes Ecommerce API"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./app/file.db"

    SECRET_KEY: str = "change_this_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    KHQR_GATEWAY_URL: str = "https://khqr.cc/api/payment/request"
    KHQR_PROFILE_ID: str = "aEaG4uiBgUg0s69AaCxGbDoldlG7OZyz"
    KHQR_SECRET_KEY: str = "YOUR_SECRET_KEY"
    KHQR_PROFILE_KEY: str = "YOUR_PROFILE_KEY"
    KHQR_VERIFY_URL: str = "https://khqr.cc/api/aEaG4uiBgUg0s69AaCxGbDoldlG7OZyz/payment-gateway/v1/payments/check-trans"
    SITE_SUCCESS_URL: str = "http://127.0.0.1:8000/api/payments/success"

    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
