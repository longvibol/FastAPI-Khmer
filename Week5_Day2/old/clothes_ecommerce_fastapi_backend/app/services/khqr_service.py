import hashlib
import json
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict
from urllib.parse import urlencode

import requests

from app.config import settings


def format_amount(amount: float) -> str:
    return str(Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def build_checkout_url(transaction_id: str, amount: float, success_url: str, remark: str = "") -> str:
    amount_text = format_amount(amount)
    raw_string = (
        settings.KHQR_SECRET_KEY
        + transaction_id
        + amount_text
        + success_url
        + remark
    )
    secure_hash = hashlib.sha1(raw_string.encode("utf-8")).hexdigest()

    payment_data = {
        "transaction_id": transaction_id,
        "amount": amount_text,
        "success_url": success_url,
        "remark": remark,
        "hash": secure_hash,
    }

    return f"{settings.KHQR_GATEWAY_URL}/{settings.KHQR_PROFILE_ID}?{urlencode(payment_data)}"


def verify_transaction(transaction_id: str) -> Dict[str, Any]:
    verify_hash = hashlib.sha1(
        (settings.KHQR_PROFILE_KEY + transaction_id).encode("utf-8")
    ).hexdigest()

    post_data = {
        "transaction_id": transaction_id,
        "hash": verify_hash,
    }

    try:
        response = requests.post(settings.KHQR_VERIFY_URL, data=post_data, timeout=15)
        response.raise_for_status()
        result = response.json()
    except Exception as exc:
        return {
            "ok": False,
            "is_paid": False,
            "status": "ERROR",
            "message": f"Could not verify payment: {exc}",
            "raw": {},
        }

    is_paid = (
        result.get("responseCode") == 0
        and isinstance(result.get("data"), dict)
        and str(result["data"].get("status", "")).lower() == "success"
    )

    return {
        "ok": True,
        "is_paid": is_paid,
        "status": result.get("data", {}).get("status", "NOT_FOUND"),
        "amount": result.get("data", {}).get("amount"),
        "message": result.get("responseMessage", "Unknown"),
        "raw": result,
        "raw_json": json.dumps(result, ensure_ascii=False),
    }
