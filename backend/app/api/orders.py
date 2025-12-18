from fastapi import APIRouter, HTTPException
from ..db.fake_data import load_orders



router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/{order_id}")
def get_order(order_id: str):
    orders = load_orders()
    for o in orders:
        if o["order_id"] == order_id:
            return o
    raise HTTPException(status_code=404, detail="Order not found")
