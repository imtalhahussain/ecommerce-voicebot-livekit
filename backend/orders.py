import json
from pathlib import Path

ORDERS_FILE = Path(__file__).parent / "data" / "orders.json"

def get_order_by_id(order_id: str):
    if not ORDERS_FILE.exists():
        return None

    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        orders = json.load(f)

    for order in orders:
        if str(order.get("order_id")) == str(order_id):
            return order

    return None
