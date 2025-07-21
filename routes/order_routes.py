from fastapi import APIRouter
from models.schemas import *
from database import order_collection, product_collection
from bson import ObjectId
from utils import to_str_id

router = APIRouter()

@router.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate):
    order_dict = order.dict()
    result = await order_collection.insert_one(order_dict)
    return {"id": str(result.inserted_id)}

@router.get("/orders/{user_id}", response_model=OrderListResponse)
async def get_orders(user_id: str, limit: int = 0, offset: int = 0):
    cursor = order_collection.find({"userId": user_id}).skip(offset).limit(limit)
    orders = []
    async for order in cursor:
        items = []
        total = 0
        for item in order["items"]:
            product = await product_collection.find_one({"_id": ObjectId(item["productId"])})
            product_detail = {
                "productDetails": {
                    "name": product["name"],
                    "id": str(product["_id"])
                },
                "qty": item["qty"]
            }
            total += product["price"] * item["qty"]
            items.append(product_detail)
        orders.append({
            "id": str(order["_id"]),
            "items": items,
            "total": total
        })

    return {
        "data": orders,
        "page": {
            "next": str(offset + limit),
            "limit": limit,
            "previous": offset - limit
        }
    }
