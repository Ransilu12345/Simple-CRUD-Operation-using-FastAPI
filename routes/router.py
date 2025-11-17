from fastapi import APIRouter, HTTPException, status, Depends, Header
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
from models.model import Model
from config.database import collection_name
from schema.schemas import item_list, get_item
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

API_KEY = os.getenv("API_KEY")

def authorize(authorization: str = Header(None, alias="Authorization")):
    """Custom Header Authorization"""
    print(f"Received Authorization Header: {authorization}")  # Debug print
    if authorization != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access"
        )


# CRUD routes with authorize dependency
@router.get("/", dependencies=[Depends(authorize)])
async def list_items():
    try:
        return item_list(collection_name.find())
    except ServerSelectionTimeoutError:
        raise HTTPException(503, "Database unavailable")
    except PyMongoError as exc:
        raise HTTPException(500, str(exc))

@router.get("/{item_id}", dependencies=[Depends(authorize)])
async def get_single_item(item_id: str):
    item = collection_name.find_one({"id": item_id})
    if not item:
        raise HTTPException(404, "Item not found")
    return get_item(item)

@router.post("/", dependencies=[Depends(authorize)])
async def create_item(item: Model):
    if item.id and collection_name.find_one({"id": item.id}):
        raise HTTPException(409, "Item with this id already exists")
    collection_name.insert_one(item.dict())
    created = collection_name.find_one({"id": item.id})
    return get_item(created) if created else item.dict()

@router.put("/{item_id}", dependencies=[Depends(authorize)])
async def update_item(item_id: str, updated: Model):
    result = collection_name.update_one({"id": item_id}, {"$set": updated.dict()})
    if result.matched_count == 0:
        raise HTTPException(404, "Item not found")
    item = collection_name.find_one({"id": item_id})
    return get_item(item) if item else updated.dict()

@router.delete("/{item_id}", status_code=204, dependencies=[Depends(authorize)])
async def delete_item(item_id: str):
    result = collection_name.delete_one({"id": item_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Item not found")
