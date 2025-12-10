from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Order(BaseModel):
    order_id: str
    user_id: Optional[str] = None
    status: str
    items: List[Dict[str, Any]]
    estimated_delivery: Optional[str] = None
    carrier: Optional[str] = None
