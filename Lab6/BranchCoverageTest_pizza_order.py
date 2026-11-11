"""Branch Coverage Test Suite for Pizza Order Application.

Student Name: Kalluri Yaswanth
SRN: PES2UG24CS212
Deliverable: Branch Coverage (>= 90%)

This test suite comprehensively exercises both True and False outcomes for all
decision structures, predicates, boundary comparisons, and error branches in
pizza_order.py.
"""

import pytest
from pizza_order import delivery_status, order_discount, pizza_price


# ============================================================================
# Branch & Boundary Tests for pizza_price
# ============================================================================

def test_pizza_price_unknown_size():
    """Branch: size not in SIZE_PRICE (True)."""
    with pytest.raises(ValueError, match="unknown size"):
        pizza_price("giant", 2, False)


def test_pizza_price_negative_toppings():
    """Branch: toppings < 0 (True)."""
    with pytest.raises(ValueError, match="invalid toppings"):
        pizza_price("small", -1, False)


def test_pizza_price_zero_toppings_small():
    """Branch: toppings <= 3 (False for toppings > 3), is_cheese_burst (False), small size."""
    # Base 200 + 0 = 200
    assert pizza_price("small", 0, False) == 200


def test_pizza_price_exact_three_toppings_boundary():
    """Branch boundary: toppings == 3 (toppings > 3 evaluates to False)."""
    # Base 350 + 3 * 40 = 470
    assert pizza_price("medium", 3, False) == 470


def test_pizza_price_four_toppings_boundary():
    """Branch boundary: toppings == 4 (toppings > 3 evaluates to True)."""
    # Base 350 + (3 * 40) + (1 * 30) = 350 + 120 + 30 = 500
    assert pizza_price("medium", 4, False) == 500


def test_pizza_price_six_toppings_large():
    """Branch: toppings > 3 with large size and no cheese burst."""
    # Base 500 + 120 + 3 * 30 = 500 + 120 + 90 = 710
    assert pizza_price("large", 6, False) == 710


def test_pizza_price_cheese_burst_small_raises_error():
    """Branch: is_cheese_burst (True) and size == 'small' (True)."""
    with pytest.raises(ValueError, match="cheese burst not available for small"):
        pizza_price("small", 2, True)


def test_pizza_price_cheese_burst_medium_valid():
    """Branch: is_cheese_burst (True) and size == 'medium' (False for size == 'small')."""
    # Base 350 + 2 * 40 (80) + 100 = 530
    assert pizza_price("medium", 2, True) == 530


def test_pizza_price_cheese_burst_large_valid():
    """Branch: is_cheese_burst (True) and size == 'large' (False for size == 'small')."""
    # Base 500 + 1 * 40 (40) + 100 = 640
    assert pizza_price("large", 1, True) == 640


# ============================================================================
# Branch & Boundary Tests for order_discount
# ============================================================================

def test_order_discount_below_minimum_boundary_299():
    """Branch boundary: order_total < 300 evaluates to True (order_total = 299)."""
    assert order_discount(299, "tuesday", True) == 0


def test_order_discount_exact_threshold_boundary_300():
    """Branch boundary: order_total < 300 evaluates to False (order_total = 300)."""
    # Tuesday, non-student: 300 // 2 = 150
    assert order_discount(300, "tuesday", False) == 150


def test_order_discount_tuesday_with_student():
    """Branch: day == 'tuesday' (True) and is_student (True)."""
    # 500 // 2 + 50 = 250 + 50 = 300
    assert order_discount(500, "tuesday", True) == 300


def test_order_discount_saturday_non_student():
    """Branch: day in ('saturday', 'sunday') (True for saturday) and is_student (False)."""
    assert order_discount(500, "saturday", False) == 0


def test_order_discount_saturday_with_student():
    """Branch: day in ('saturday', 'sunday') (True for saturday) and is_student (True)."""
    # 0 + 50 = 50
    assert order_discount(500, "saturday", True) == 50


def test_order_discount_sunday_non_student():
    """Branch: day in ('saturday', 'sunday') (True for sunday) and is_student (False)."""
    assert order_discount(600, "sunday", False) == 0


def test_order_discount_sunday_with_student():
    """Branch: day in ('saturday', 'sunday') (True for sunday) and is_student (True)."""
    # 0 + 50 = 50
    assert order_discount(600, "sunday", True) == 50


def test_order_discount_weekday_other_non_student():
    """Branch: else day (neither tuesday nor weekend), is_student (False)."""
    # 450 // 10 = 45
    assert order_discount(450, "wednesday", False) == 45


def test_order_discount_weekday_other_with_student():
    """Branch: else day (neither tuesday nor weekend), is_student (True)."""
    # 450 // 10 + 50 = 45 + 50 = 95
    assert order_discount(450, "thursday", True) == 95


# ============================================================================
# Branch & Boundary Tests for delivery_status
# ============================================================================

def test_delivery_status_distance_exceeded():
    """Branch: distance_km > 10 (True)."""
    assert delivery_status(20, 11) == "not deliverable"


def test_delivery_status_distance_exact_ten_boundary():
    """Branch boundary: distance_km == 10 (distance_km > 10 evaluates to False)."""
    # minutes 25 <= 30 -> on time
    assert delivery_status(25, 10) == "on time"


def test_delivery_status_on_time_exact_thirty_boundary():
    """Branch boundary: minutes_taken == 30 (minutes_taken <= 30 evaluates to True)."""
    assert delivery_status(30, 5) == "on time"


def test_delivery_status_late_exact_thirty_one_boundary():
    """Branch boundary: minutes_taken == 31 (> 30 and <= 45)."""
    assert delivery_status(31, 5) == "late"


def test_delivery_status_late_exact_forty_five_boundary():
    """Branch boundary: minutes_taken == 45 (minutes_taken <= 45 evaluates to True)."""
    assert delivery_status(45, 5) == "late"


def test_delivery_status_free_pizza_exact_forty_six_boundary():
    """Branch boundary: minutes_taken == 46 (> 45 evaluates to True for free pizza)."""
    assert delivery_status(46, 5) == "free pizza"


def test_delivery_status_free_pizza_high_duration():
    """Branch: minutes_taken well beyond 45 minutes."""
    assert delivery_status(75, 4) == "free pizza"
