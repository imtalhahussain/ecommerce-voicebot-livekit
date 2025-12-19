import re

# Mock order database
ORDERS = {
    "ORT1001": "Your order ORT-1001 is out for delivery and will arrive today.",
    "ORT1002": "Your order ORT-1002 has been delivered successfully.",
    "ORT1003": "Your order ORT-1003 is currently being packed."
}


def normalize_order_id(text: str) -> str | None:
    """
    Normalize spoken order IDs like:
    - 'O R T 1 0 0 1'
    - 'ORT 1001'
    - '1,001'
    - 'order 1001'
    """

    text = text.upper()

    # Remove commas and spaces
    cleaned = re.sub(r"[,\s]", "", text)

    # Extract digits
    digits = re.findall(r"\d+", cleaned)
    if not digits:
        return None

    number = digits[-1]

    # Assume ORT prefix if not spoken clearly
    return f"ORT{number}"


def rag_search(query: str) -> str | None:
    order_id = normalize_order_id(query)

    if not order_id:
        print(" RAG MISS (no order id detected)")
        return None

    if order_id in ORDERS:
        print(f" RAG HIT: {order_id}")
        return ORDERS[order_id]

    print(f" RAG MISS: {order_id}")
    return None
