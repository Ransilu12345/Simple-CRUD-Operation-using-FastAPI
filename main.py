"""Application entrypoint that wires the API router into FastAPI."""
from fastapi import FastAPI
from routes.router import router

# Initialize the FastAPI application.
app = FastAPI()

# Mount the CRUD routes. Add `prefix="/items"` here if you want a base path.
app.include_router(router)

