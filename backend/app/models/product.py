from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    currency: str = "INR"
    category: Optional[str] = None
