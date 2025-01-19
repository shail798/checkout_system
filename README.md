# Supermarket Checkout System

A FastAPI-based checkout system API that handles special pricing rules and item management.

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pydantic

# Run server
python main.py
```

Server runs at `http://localhost:8000`

## API Endpoints

### 1. Process Checkout
Calculate total for items
```bash
curl -X POST http://localhost:8000/api/v1/checkout \
  -H "Content-Type: application/json" \
  -d '{"items": "AAABBD"}'
```

### 2. View All Prices
Get current prices and offers
```bash
curl -X GET http://localhost:8000/api/v1/prices
```

### 3. Add New Item
Add item with pricing rules
```bash
curl -X POST "http://localhost:8000/api/v1/items?item_id=E" \
  -H "Content-Type: application/json" \
  -d '{
    "unit_price": 40,
    "special_quantity": 3,
    "special_price": 100
  }'
```

### 4. Update Item Price
Change unit price of an item
```bash
curl -X PUT "http://localhost:8000/api/v1/items/A/price?unit_price=55"
```

### 5. Set Special Price
Add/update special pricing
```bash
curl -X PUT "http://localhost:8000/api/v1/items/C/special-price" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 3,
    "price": 50
  }'
```

### 6. Remove Special Price
Remove special pricing from item
```bash
curl -X DELETE "http://localhost:8000/api/v1/items/B/special-price"
```

### 7. Delete Item
Remove item completely
```bash
curl -X DELETE "http://localhost:8000/api/v1/items/D"
```

## Default Items

- A: 50 each or 3 for 130
- B: 30 each or 2 for 45
- C: 20 each
- D: 15 each

## Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing
```bash
pytest tests/
``` 