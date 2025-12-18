from fastapi import APIRouter
from ..db.fake_data import load_products

 

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/search")
def search_products(payload: dict):
    q = (payload.get("query") or "").lower()
    limit = int(payload.get("limit", 5))

    products = load_products()
    results = [
        p for p in products
        if q in (p.get("name", "") + p.get("description", "")).lower()
    ][:limit]

    return {"results": results}
