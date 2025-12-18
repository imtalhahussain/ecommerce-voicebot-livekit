# agent/tools/__init__.py

def search_products(query: str):
    """
    Mock product search.
    Replace with DB / API / RAG later.
    """
    return [
        {"name": "Nike Run Swift", "price": 2899},
        {"name": "Adidas Duramo SL", "price": 2599},
        {"name": "Puma Velocity Nitro", "price": 2999},
    ]


def track_order(order_id: str):
    """
    Mock order tracking.
    """
    return {
        "order_id": order_id,
        "status": "Out for delivery",
        "expected_delivery": "Tomorrow",
    }
