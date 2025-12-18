# agent/tools/__init__.py

from typing import List, Dict


def search_products(query: str) -> List[Dict]:
    """
    Structured product search result.
    """
    return [
        {
            "id": "SKU123",
            "name": "Nike Run Swift",
            "price": 2899,
            "category": "Running Shoes",
            "in_stock": True,
        },
        {
            "id": "SKU124",
            "name": "Adidas Duramo SL",
            "price": 2599,
            "category": "Running Shoes",
            "in_stock": True,
        },
        {
            "id": "SKU125",
            "name": "Puma Velocity Nitro",
            "price": 2999,
            "category": "Running Shoes",
            "in_stock": False,
        },
    ]


def track_order(order_id: str) -> Dict:
    """
    Structured order tracking result.
    """
    return {
        "order_id": order_id,
        "status": "Out for delivery",
        "expected_delivery": "Tomorrow",
        "courier": "Delhivery",
    }
