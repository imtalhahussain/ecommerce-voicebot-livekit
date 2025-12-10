from pathlib import Path
import json

ROOT = Path(__file__).parent.parent.parent
DATA_DIR = ROOT / "data"

def load_products():
    path = DATA_DIR / "products.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))

def load_orders():
    path = DATA_DIR / "orders.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))
