from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Optional

from app.api.schemas.cart_schema import (
    CheckoutRequest, 
    CheckoutResponse, 
    PricingRuleRequest, 
    SpecialPriceRequest
)
from app.services.checkout_service import CheckoutService
from app.models.pricing import pricing_repository  # Import the singleton

router = APIRouter()

def get_checkout_service():
    # Dependency injection using the singleton repository
    return CheckoutService(pricing_repository)

@router.post("/checkout", response_model=CheckoutResponse)
async def process_checkout(
    request: CheckoutRequest,
    checkout_service: CheckoutService = Depends(get_checkout_service)
):
    # Process checkout and return total price
    try:
        total = checkout_service.calculate_total(request.items)
        return CheckoutResponse(total=total)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/prices")
async def get_prices(
    checkout_service: CheckoutService = Depends(get_checkout_service)
) -> Dict[str, Dict]:
    # Get all available items and their prices
    rules = checkout_service.pricing_rules.get_all_rules()
    return {
        item: {
            "unit_price": rule.unit_price,
            "special_offer": f"{rule.special_quantity} for {rule.special_price}"
            if rule.special_quantity and rule.special_price
            else None
        }
        for item, rule in rules.items()
    }

@router.post("/items", status_code=status.HTTP_201_CREATED)
async def add_item(
    item_id: str,
    pricing: PricingRuleRequest,
    checkout_service: CheckoutService = Depends(get_checkout_service)
):
    # Add a new item with its pricing
    if len(item_id) != 1 or not item_id.isalpha():
        raise HTTPException(
            status_code=400,
            detail="Item ID must be a single alphabetical character"
        )
    return checkout_service.add_item(item_id.upper(), pricing)

@router.put("/items/{item_id}/price")
async def update_unit_price(
    item_id: str,
    unit_price: int,
    checkout_service: CheckoutService = Depends(get_checkout_service)
):
    # Update unit price for an item
    try:
        return checkout_service.update_unit_price(item_id.upper(), unit_price)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/items/{item_id}/special-price")
async def set_special_price(
    item_id: str,
    special_price: SpecialPriceRequest,
    checkout_service: CheckoutService = Depends(get_checkout_service)
):
    # Set or update special price for an item
    try:
        return checkout_service.set_special_price(
            item_id.upper(), 
            special_price.quantity, 
            special_price.price
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/items/{item_id}/special-price")
async def remove_special_price(
    item_id: str,
    checkout_service: CheckoutService = Depends(get_checkout_service)
):
    # Remove special price for an item
    try:
        return checkout_service.remove_special_price(item_id.upper())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/items/{item_id}")
async def delete_item(
    item_id: str,
    checkout_service: CheckoutService = Depends(get_checkout_service)
):
    # Delete an item and its pricing rules
    try:
        return checkout_service.delete_item(item_id.upper())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 