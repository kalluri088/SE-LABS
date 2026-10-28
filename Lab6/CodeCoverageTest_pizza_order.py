"""Code Coverage Test Suite for Pizza Order Application.

Student Name: Kalluri Yaswanth
SRN: PES2UG24CS212
Deliverable: Code Coverage (>= 90%)
"""

import pytest
from pizza_order import delivery_status, order_discount, pizza_price


# ============================================================================
# Tests for pizza_price
# ============================================================================

def test_pizza_price_invalid_size():
    """Test unknown size raises ValueError."""
    with pytest.raises(ValueError, match="unknown size"):
        pizza_price("extra_large", 2, False)


def test_pizza_price_negative_toppings():
    """Test negative toppings count raises ValueError."""
    with pytest.raises(ValueError, match="invalid toppings"):
        pizza_price("medium", -1, False)


def test_pizza_price_standard_toppings():
    """Test normal pizza pricing with <= 3 toppings."""
    # medium = 350, toppings = 2 * 40 = 80 -> total = 430
    assert pizza_price("medium", 2, False) == 430


def test_pizza_price_excess_toppings():
    """Test tiered toppings calculation when toppings > 3."""
    # large = 500, toppings = 5 -> 3 * 40 + 2 * 30 = 180 -> total = 680
    assert pizza_price("large", 5, False) == 680


def test_pizza_price_cheese_burst_small_disallowed():
    """Test cheese burst requested on small size raises ValueError."""
    with pytest.raises(ValueError, match="cheese burst not available for small"):
        pizza_price("small", 1, True)


def test_pizza_price_cheese_burst_valid():
    """Test cheese burst surcharge on valid pizza size."""
    # medium = 350, 1 topping = 40, cheese burst = 100 -> total = 490
    assert pizza_price("medium", 1, True) == 490


# ============================================================================
# Tests for order_discount
# ============================================================================

def test_order_discount_below_threshold():
    """Test order total below 300 receives zero discount."""
    assert order_discount(250, "tuesday", False) == 0


def test_order_discount_tuesday():
    """Test Tuesday 50% discount for non-student."""
    # 400 // 2 = 200
    assert order_discount(400, "tuesday", False) == 200


def test_order_discount_weekend_saturday():
    """Test Saturday orders receive zero base discount."""
    assert order_discount(500, "saturday", False) == 0


def test_order_discount_weekend_sunday():
    """Test Sunday orders receive zero base discount."""
    assert order_discount(500, "sunday", False) == 0


def test_order_discount_weekday_standard():
    """Test weekday 10% discount for non-student."""
    # 400 // 10 = 40
    assert order_discount(400, "monday", False) == 40


def test_order_discount_student_additional():
    """Test student extra discount addition."""
    # 400 on monday: 40 + 50 = 90
    assert order_discount(400, "monday", True) == 90


# ============================================================================
# Tests for delivery_status
# ============================================================================

def test_delivery_status_distance_exceeded():
    """Test distance > 10 km returns not deliverable."""
    assert delivery_status(25, 12) == "not deliverable"


def test_delivery_status_on_time():
    """Test delivery completed within 30 minutes."""
    assert delivery_status(25, 5) == "on time"


def test_delivery_status_late():
    """Test delivery between 31 and 45 minutes."""
    assert delivery_status(35, 5) == "late"


def test_delivery_status_free_pizza():
    """Test delivery exceeding 45 minutes qualifies for free pizza."""
    assert delivery_status(50, 5) == "free pizza"
