def is_product_query(text: str) -> bool:
    keywords = ["buy", "price", "shoe", "shoes", "order", "running"]
    text = text.lower()
    return any(k in text for k in keywords)
