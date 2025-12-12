def is_product_query(text: str) -> bool:
    text = text.lower()
    keywords = ["shoes", "sneaker", "buy", "running", "price", "under", "recommend", "best"]
    return any(k in text for k in keywords)
