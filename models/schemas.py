from pydantic import BaseModel
from typing import List, Optional

class Size(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[Size]

class ProductResponse(BaseModel):
    id: str

class ProductListItem(BaseModel):
    id: str
    name: str
    price: float

class ProductListResponse(BaseModel):
    data: List[ProductListItem]
    page: dict

class OrderItem(BaseModel):
    productId: str
    qty: int

class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]

class OrderResponse(BaseModel):
    id: str

class ProductDetail(BaseModel):
    name: str
    id: str

class OrderListItem(BaseModel):
    id: str
    items: List[dict]
    total: float

class OrderListResponse(BaseModel):
    data: List[OrderListItem]
    page: dict
