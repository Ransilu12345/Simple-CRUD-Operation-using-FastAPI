"""Database connection setup for MongoDB using PyMongo."""

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB running in Docker
client = MongoClient(os.getenv("MONGODB_URI"))

# Select the `memory` database.
db = client.memory

# Use the `chat_history` collection to store BAeModels items.
collection_name = db["chat_history"]
