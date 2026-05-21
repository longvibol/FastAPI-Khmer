import hashlib
import requests
from urllib.parse import urlencode
from app.config import settings


def create_checkout_url(transaction_id: str, amount: float, remark: str = "Web Order") -> str:
    amount_str = f"{amount:.2f}"
    raw_string = (
        settings.KHQR_SECRET_KEY
        + transaction_id
        + amount_str
        + settings.SITE_SUCCESS_URL
        + remark
    )
    secure_hash = hashlib.sha1(raw_string.encode()).hexdigest()

    params = {
        "transaction_id": transaction_id,
        "amount": amount_str,
        "success_url": settings.SITE_SUCCESS_URL,
        "remark": remark,
        "hash": secure_hash,
    }
    return f"{settings.KHQR_GATEWAY_URL}/{settings.KHQR_PROFILE_ID}?{urlencode(params)}"


def verify_transaction(transaction_id: str) -> dict:
    secure_hash = hashlib.sha1((settings.KHQR_PROFILE_KEY + transaction_id).encode()).hexdigest()
    post_data = {
        "transaction_id": transaction_id,
        "hash": secure_hash,
    }
    try:
        response = requests.post(settings.KHQR_VERIFY_URL, data=post_data, timeout=20)
        return response.json()
    except Exception as e:
        return {
            "responseCode": 1,
            "responseMessage": f"Verification request failed: {str(e)}",
        }


def is_payment_success(result: dict) -> bool:
    return (
        result.get("responseCode") == 0
        and str(result.get("data", {}).get("status", "")).lower() == "success"
    )
