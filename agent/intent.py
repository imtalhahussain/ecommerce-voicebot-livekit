def detect_intent(text: str) -> str:
    t = text.lower()
    if "order" in t:
        return "order_status"
    if any(k in t for k in ["buy", "price", "shoe", "shoes"]):
        return "product_search"
    return "general"
