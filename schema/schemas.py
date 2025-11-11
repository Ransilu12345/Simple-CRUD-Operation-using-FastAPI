"""Helper functions to map MongoDB documents into API-safe dictionaries.

These mappings avoid leaking Mongo-specific fields like `_id` and ensure
consistent shapes in API responses.
"""
from typing import Any, Dict, Iterable, List


def get_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a single MongoDB document into a public API dictionary."""
    return {
        "id": str(item.get("id")),
        "name": item.get("name"),
        "email": item.get("email"),
        "message": item.get("message"),
        "summary": item.get("summary"),
    }

def item_list(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert an iterable of documents (e.g., a cursor) into a list of dicts."""
    return [get_item(item) for item in items]