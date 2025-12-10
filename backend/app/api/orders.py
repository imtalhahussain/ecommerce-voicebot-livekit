from fastapi import APIRouter, HTTPException
from ..db.fake_data import load_orders

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/{order_id}")
def get_order(order_id: str):
    orders = load_orders()
    order_map = {o["order_id"]: o for o in orders}
    order = order_map.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
