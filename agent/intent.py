from enum import Enum


class Intent(str, Enum):
    PRODUCT_SEARCH = "product_search"
    ORDER_TRACKING = "order_tracking"
    GENERAL_CHAT = "general_chat"


def detect_intent(text: str) -> Intent:
    t = text.lower()

    if any(k in t for k in ["buy", "price", "cost", "under", "shoes", "running", "product"]):
        return Intent.PRODUCT_SEARCH

    if any(k in t for k in ["order", "track", "delivery", "shipped", "status"]):
        return Intent.ORDER_TRACKING

    return Intent.GENERAL_CHAT
