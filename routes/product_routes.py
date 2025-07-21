from fastapi import APIRouter, Query
from models.schemas import *
from database import product_collection
from bson import ObjectId
from utils import to_str_id

router = APIRouter()

@router.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate):
    result = await product_collection.insert_one(product.dict())
    return {"id": str(result.inserted_id)}

@router.get("/products", response_model=ProductListResponse)
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 0,
    offset: int = 0,
):
    query = {}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes"] = {"$elemMatch": {"size": size}}

    cursor = product_collection.find(query).skip(offset).limit(limit)
    products = []
    async for product in cursor:
        products.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"]
        })

    return {
        "data": products,
        "page": {
            "next": str(offset + limit),
            "limit": limit,
            "previous": offset - limit
        }
    }
