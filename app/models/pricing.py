from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class PricingRule:
    # Class to hold pricing rules for an item
    unit_price: int
    special_quantity: Optional[int] = None
    special_price: Optional[int] = None

    def calculate_price(self, quantity: int) -> int:
        # Calculate total price for a given quantity of items
        if not self.special_quantity or not self.special_price:
            return quantity * self.unit_price
            
        sets = quantity // self.special_quantity
        remainder = quantity % self.special_quantity
        
        return (sets * self.special_price) + (remainder * self.unit_price)

class PricingRuleRepository:
    # Repository for storing and retrieving pricing rules
    def __init__(self):
        self.rules: Dict[str, PricingRule] = {
            'A': PricingRule(unit_price=50, special_quantity=3, special_price=130),
            'B': PricingRule(unit_price=30, special_quantity=2, special_price=45),
            'C': PricingRule(unit_price=20),
            'D': PricingRule(unit_price=15)
        }
    
    def get_rule(self, item: str) -> Optional[PricingRule]:
        # Get pricing rule for an item
        return self.rules.get(item)

    def get_all_rules(self) -> Dict[str, PricingRule]:
        # Get all pricing rules
        return self.rules

    def add_rule(self, item: str, rule: PricingRule) -> Dict:
        # Add a new pricing rule
        self.rules[item] = rule
        return self._rule_to_dict(item, rule)

    def update_rule(self, item: str, rule: PricingRule) -> Dict:
        # Update an existing pricing rule
        self.rules[item] = rule
        return self._rule_to_dict(item, rule)

    def delete_rule(self, item: str) -> Dict:
        # Delete a pricing rule
        rule = self.rules.pop(item)
        return self._rule_to_dict(item, rule)

    def _rule_to_dict(self, item: str, rule: PricingRule) -> Dict:
        # Convert rule to dictionary format
        return {
            "item": item,
            "unit_price": rule.unit_price,
            "special_quantity": rule.special_quantity,
            "special_price": rule.special_price
        }

# Create singleton instance
pricing_repository = PricingRuleRepository() 