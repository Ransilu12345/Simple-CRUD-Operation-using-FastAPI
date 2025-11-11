"""FastAPI routes implementing CRUD operations for chat history items."""
from fastapi import APIRouter, HTTPException, status
from models.model import BAeModels
from config.database import collection_name
from schema.schemas import item_list, get_item
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
async def list_items():
    """Return all items in the collection."""
    try:
        items = item_list(collection_name.find())
        return items
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")
    except PyMongoError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

@router.get("/{item_id}", status_code=status.HTTP_200_OK)
async def get_single_item(item_id: str):
    """Return a single item by its application-level id."""
    try:
        item = collection_name.find_one({"id": item_id})
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return get_item(item)
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")
    except PyMongoError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(item: BAeModels):
    """Create a new item. Conflicts if an item with the same id already exists."""
    try:
        existing = collection_name.find_one({"id": item.id})
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item with this id already exists")
        collection_name.insert_one(dict(item))
        created = collection_name.find_one({"id": item.id})
        return get_item(created) if created else dict(item)
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")
    except PyMongoError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

@router.put("/{item_id}", status_code=status.HTTP_200_OK)
async def update_item(item_id: str, updated: BAeModels):
    """Replace an item by id with the provided payload."""
    try:
        result = collection_name.update_one({"id": item_id}, {"$set": dict(updated)})
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        item = collection_name.find_one({"id": item_id})
        return get_item(item) if item else dict(updated)
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")
    except PyMongoError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str):
    """Delete an item by its id. Returns 204 on success."""
    try:
        result = collection_name.delete_one({"id": item_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return None
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")
    except PyMongoError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))