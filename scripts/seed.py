"""Seed the MongoDB collection with sample BAeModels data.

Run:
    python scripts/seed.py
"""
import os
import sys
from typing import Any, Dict, List

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config.database import collection_name  # noqa: E402


def get_sample_items() -> List[Dict[str, Any]]:
    """Return a list of sample items matching BAeModels shape."""
    return [
        {
            "id": "mem-001",
            "name": "Alice",
            "email": "alice@example.com",
            "message": "Hello there",
            "summary": "Greeting",
        },
        {
            "id": "mem-002",
            "name": "Bob",
            "email": "bob@example.com",
            "message": "Memory note",
            "summary": None,
        },
        {
            "id": "mem-003",
            "name": "Carol",
            "email": "carol@example.com",
            "message": "Another message",
            "summary": "Short memo",
        },
    ]


def seed_sample_data() -> None:
    """Upsert each sample item by its application-level id."""
    sample_items = get_sample_items()
    inserted = 0
    skipped = 0

    for item in sample_items:
        result = collection_name.update_one(
            {"id": item["id"]},
            {"$setOnInsert": item},
            upsert=True,
        )
        if result.upserted_id is not None:
            inserted += 1
        else:
            skipped += 1

    print(f"Done. Inserted: {inserted}, Skipped (already exists): {skipped}")


if __name__ == "__main__":
    seed_sample_data()

