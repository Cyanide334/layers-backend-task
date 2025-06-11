from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class Order:
    sku_id: str
    delivered_at: datetime

# In-memory storage for Orders with uniqueness constraints
order_store: List[Order] = []
order_by_sku: Dict[str, Order] = {}  # For unique sku_id lookup

def add_or_update_order(order: Order) -> None:
    """
    Add a new order or update an existing one for the same SKU.
    """
    if order.sku_id in order_by_sku:
        # Update existing order
        existing_order = order_by_sku[order.sku_id]
        existing_order.delivered_at = order.delivered_at
    else:
        # Add new order
        order_store.append(order)
        order_by_sku[order.sku_id] = order

def get_order_by_sku(sku_id: str) -> Order:
    """Get order by SKU ID"""
    return order_by_sku.get(sku_id) 