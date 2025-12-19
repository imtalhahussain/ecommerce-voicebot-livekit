from enum import Enum

class Intent(Enum):
    GENERAL_CHAT = "general_chat"
    PRODUCT_SEARCH = "product_search"
    ORDER_TRACKING = "order_tracking"


def detect_intent(text: str) -> Intent:
    t = text.lower()
    if "order" in t or "track" in t:
        return Intent.ORDER_TRACKING
    if "shoe" in t or "product" in t or "show me" in t:
        return Intent.PRODUCT_SEARCH
    return Intent.GENERAL_CHAT
