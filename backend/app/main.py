from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import products, orders  # ensure package import works

app = FastAPI(title="Ecommerce Voicebot Backend", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)

@app.get("/health")
def health():
    return {"status":"ok"}
