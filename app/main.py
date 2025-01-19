from fastapi import FastAPI
from app.api.routes import checkout

app = FastAPI(
    title="Supermarket Checkout API",
    description="API for calculating checkout totals with special pricing rules",
    version="1.0.0"
)

app.include_router(checkout.router, prefix="/api/v1", tags=["checkout"]) 