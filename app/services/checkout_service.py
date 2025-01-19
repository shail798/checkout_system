from collections import Counter
from typing import Optional, Dict

from app.models.pricing import PricingRuleRepository, PricingRule

class CheckoutService:
    # Service class that handles checkout business logic
    def __init__(self, pricing_rules: PricingRuleRepository):
        self.pricing_rules = pricing_rules
    
    def calculate_total(self, items: str) -> float:
        # Calculate total price for a string of items
        if not items:
            return 0
            
        item_counts = Counter(items)
        total = 0
        
        for item, count in item_counts.items():
            rule = self.pricing_rules.get_rule(item)
            if not rule:
                raise ValueError(f"Invalid item: {item}")
            total += rule.calculate_price(count)
            
        return total

    def add_item(self, item_id: str, pricing_data: Dict) -> Dict:
        # Add a new item with pricing rules
        if self.pricing_rules.get_rule(item_id):
            raise ValueError(f"Item {item_id} already exists")
        
        rule = PricingRule(
            unit_price=pricing_data.unit_price,
            special_quantity=pricing_data.special_quantity,
            special_price=pricing_data.special_price
        )
        return self.pricing_rules.add_rule(item_id, rule)

    def update_unit_price(self, item_id: str, unit_price: int) -> Dict:
        # Update unit price for an item
        rule = self.pricing_rules.get_rule(item_id)
        if not rule:
            raise ValueError(f"Item {item_id} not found")
        
        rule.unit_price = unit_price
        return self.pricing_rules.update_rule(item_id, rule)

    def set_special_price(self, item_id: str, quantity: int, price: int) -> Dict:
        # Set or update special price for an item
        rule = self.pricing_rules.get_rule(item_id)
        if not rule:
            raise ValueError(f"Item {item_id} not found")
        
        rule.special_quantity = quantity
        rule.special_price = price
        return self.pricing_rules.update_rule(item_id, rule)

    def remove_special_price(self, item_id: str) -> Dict:
        # Remove special price for an item
        rule = self.pricing_rules.get_rule(item_id)
        if not rule:
            raise ValueError(f"Item {item_id} not found")
        
        rule.special_quantity = None
        rule.special_price = None
        return self.pricing_rules.update_rule(item_id, rule)

    def delete_item(self, item_id: str) -> Dict:
        # Delete an item and its pricing rules
        if not self.pricing_rules.get_rule(item_id):
            raise ValueError(f"Item {item_id} not found")
        
        return self.pricing_rules.delete_rule(item_id) 