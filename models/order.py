from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Order:
    sku_id: str
    delivered_at: datetime

# In-memory storage for Orders
order_store: List[Order] = [] 