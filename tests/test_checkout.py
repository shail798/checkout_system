import pytest
from app.services.checkout_service import CheckoutService
from app.models.pricing import PricingRuleRepository

@pytest.fixture
def checkout_service():
    return CheckoutService(PricingRuleRepository())

def test_empty_checkout(checkout_service):
    assert checkout_service.calculate_total("") == 0

def test_single_items(checkout_service):
    assert checkout_service.calculate_total("A") == 50
    assert checkout_service.calculate_total("B") == 30
    assert checkout_service.calculate_total("C") == 20
    assert checkout_service.calculate_total("D") == 15

def test_multiple_items(checkout_service):
    test_cases = [
        ("AB", 80),
        ("CDBA", 115),
        ("AA", 100),
        ("AAA", 130),
        ("AAAA", 180),
        ("AAAAA", 230),
        ("AAAAAA", 260),
        ("AAAB", 160),
        ("AAABB", 175),
        ("AAABBD", 190),
        ("DABABA", 190)
    ]
    
    for items, expected in test_cases:
        assert checkout_service.calculate_total(items) == expected

def test_invalid_item(checkout_service):
    with pytest.raises(ValueError):
        checkout_service.calculate_total("Z") 