from fastapi import APIRouter
from typing import List
from ..db.fake_data import load_products

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/search")
def search_products(payload: dict):
    """
    POST /products/search
    body: {"query": "...", "max_price": 3000, "category": "running_shoes", "limit": 10}
    """
    q = (payload.get("query") or "").strip().lower()
    max_price = payload.get("max_price")
    category = (payload.get("category") or "").strip().lower() if payload.get("category") else None
    limit = int(payload.get("limit", 10))

    products = load_products()
    results = []
    for p in products:
        name = (p.get("name") or "").lower()
        desc = (p.get("description") or "").lower()
        cat = (p.get("category") or "").lower()
        if q in name or q in desc or (category and category in cat) or (not q and not category):
            if max_price and p.get("price", 0) > max_price:
                continue
            results.append(p)
        if len(results) >= limit:
            break

    return {"query": payload.get("query", ""), "results": results}
