"""Database connection setup for MongoDB using PyMongo."""

from pymongo import MongoClient

# Connect to MongoDB running in Docker
client = MongoClient("mongodb://localhost:27017/")

# Select the `memory` database.
db = client.memory

# Use the `chat_history` collection to store BAeModels items.
collection_name = db["chat_history"]
