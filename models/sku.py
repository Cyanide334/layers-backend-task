from dataclasses import dataclass
from typing import List

@dataclass
class SKU:
    sku_id: str
    barcode: str
    title: str
    brand: str
    image_url: str
    tags: List[str]

# In-memory storage for SKUs
sku_store: List[SKU] = [] 