# Low-Level Design - Supermarket Checkout System

## 1. Component Details

### 1.1 Models
```python
class PricingRule:
    - unit_price: int
    - special_quantity: Optional[int]
    - special_price: Optional[int]
    + calculate_price(quantity: int) -> int
```

### 1.2 Repository
```python
class PricingRuleRepository:
    - rules: Dict[str, PricingRule]
    + get_rule(item: str) -> Optional[PricingRule]
    + get_all_rules() -> Dict[str, PricingRule]
    + add_rule(item: str, rule: PricingRule) -> Dict
    + update_rule(item: str, rule: PricingRule) -> Dict
    + delete_rule(item: str) -> Dict
```

### 1.3 Service Layer
```python
class CheckoutService:
    - pricing_rules: PricingRuleRepository
    + calculate_total(items: str) -> float
    + add_item(item_id: str, pricing_data: Dict) -> Dict
    + update_unit_price(item_id: str, price: int) -> Dict
    + set_special_price(item_id: str, quantity: int, price: int) -> Dict
    + remove_special_price(item_id: str) -> Dict
    + delete_item(item_id: str) -> Dict
```

## 2. Data Structures

### 2.1 Request/Response Models
```python
class CheckoutRequest:
    items: str  # e.g., "AAABBD"

class CheckoutResponse:
    total: float

class PricingRuleRequest:
    unit_price: int
    special_quantity: Optional[int]
    special_price: Optional[int]

class SpecialPriceRequest:
    quantity: int
    price: int
```

## 3. API Endpoints

### 3.1 Checkout Operations
```
POST /api/v1/checkout
GET /api/v1/prices
```

### 3.2 Item Management
```
POST /api/v1/items
PUT /api/v1/items/{item_id}/price
PUT /api/v1/items/{item_id}/special-price
DELETE /api/v1/items/{item_id}/special-price
DELETE /api/v1/items/{item_id}
```

## 4. Algorithms

### 4.1 Price Calculation
```python
def calculate_price(quantity, unit_price, special_quantity, special_price):
    if not special_quantity or not special_price:
        return quantity * unit_price
        
    sets = quantity // special_quantity
    remainder = quantity % special_quantity
    
    return (sets * special_price) + (remainder * unit_price)
```

## 5. Validation Rules

### 5.1 Item Validation
- Item IDs must be single alphabetical characters
- Items must exist in repository for checkout
- Prices must be positive integers

### 5.2 Special Price Validation
- Special quantity must be > 1
- Special price must be > 0
- Special price must be less than (unit_price * quantity)

## 6. Error Handling
- 400: Bad Request (Invalid input)
- 404: Not Found (Item not found)
- 500: Internal Server Error

## 7. Data Storage
Current implementation uses in-memory storage with the following structure:
```python
rules = {
    'A': PricingRule(unit_price=50, special_quantity=3, special_price=130),
    'B': PricingRule(unit_price=30, special_quantity=2, special_price=45),
    ...
}
``` 