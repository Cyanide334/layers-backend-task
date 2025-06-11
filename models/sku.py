from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SKU:
    sku_id: str
    barcode: str
    title: str
    brand: str
    image_url: str
    tags: List[str]

# In-memory storage for SKUs with uniqueness constraints
sku_store: List[SKU] = []
sku_by_id: Dict[str, SKU] = {}  # For unique sku_id lookup
sku_by_barcode: Dict[str, SKU] = {}  # For unique barcode lookup

def add_sku(sku: SKU) -> bool:
    """
    Add a SKU to the store if it doesn't violate uniqueness constraints.
    Returns True if added successfully, False if constraints violated.
    """
    if sku.sku_id in sku_by_id or sku.barcode in sku_by_barcode:
        return False
    
    sku_store.append(sku)
    sku_by_id[sku.sku_id] = sku
    sku_by_barcode[sku.barcode] = sku
    return True

def get_sku_by_id(sku_id: str) -> SKU:
    """Get SKU by ID"""
    return sku_by_id.get(sku_id)

def get_sku_by_barcode(barcode: str) -> SKU:
    """Get SKU by barcode"""
    return sku_by_barcode.get(barcode) 