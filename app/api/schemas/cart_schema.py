from pydantic import BaseModel, field_validator
from typing import Optional
from app.models.pricing import pricing_repository  # Import the singleton repository

class CheckoutRequest(BaseModel):
    # Schema for checkout request
    items: str

    @field_validator('items')
    def validate_items(cls, v):
        # Get all valid items from the pricing repository
        valid_items = pricing_repository.get_all_rules().keys()
        if not all(c in valid_items for c in v):
            raise ValueError(f'Items must only contain letters from: {", ".join(sorted(valid_items))}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "items": "AAABBD"
            }
        }

class CheckoutResponse(BaseModel):
    # Schema for checkout response
    total: float

    class Config:
        json_schema_extra = {
            "example": {
                "total": 190
            }
        }

class PricingRuleRequest(BaseModel):
    # Schema for creating/updating pricing rules
    unit_price: int
    special_quantity: Optional[int] = None
    special_price: Optional[int] = None

    @field_validator('unit_price')
    def validate_unit_price(cls, v):
        if v <= 0:
            raise ValueError('Unit price must be greater than 0')
        return v

    @field_validator('special_price')
    def validate_special_price(cls, v, info):
        if v is not None:
            if v <= 0:
                raise ValueError('Special price must be greater than 0')
            # Get the special_quantity from the data
            special_quantity = info.data.get('special_quantity')
            if special_quantity is None:
                raise ValueError('Special quantity must be set when special price is provided')
        return v

class SpecialPriceRequest(BaseModel):
    # Schema for special price updates
    quantity: int
    price: int

    @field_validator('quantity')
    def validate_quantity(cls, v):
        if v <= 1:
            raise ValueError('Special quantity must be greater than 1')
        return v

    @field_validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Special price must be greater than 0')
        return v 