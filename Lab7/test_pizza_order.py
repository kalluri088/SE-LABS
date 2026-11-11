"""Software Engineering Lab 7: Fuzz Testing with Hypothesis.

Student Name: Kalluri Yaswanth
SRN: PES2UG24CS212
Assigned Application: pizza_order.py (L6_L7_24_pizza_order)
"""

from hypothesis import given, strategies as st
from pizza_order import toppings_price, pizza_inches, split_bill


# ---------------------------------------------------------------------------
# Stage 2/3/5: Hypothesis Property-Based Fuzz Tests (No-Crash Properties)
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_toppings_price_no_crash(s):
    """Verify that toppings_price does not crash when supplied with arbitrary
    Unicode strings, empty strings, whitespace, or None."""
    try:
        result = toppings_price(s)
        assert isinstance(result, (int, float))
        assert result >= 0
    except Exception as e:
        assert False, f"toppings_price crashed with {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_pizza_inches_no_crash(s):
    """Verify that pizza_inches does not crash on malformed, unknown, or None
    inputs, returning valid inches or fallback 0."""
    try:
        result = pizza_inches(s)
        assert isinstance(result, int)
        assert result in (0, 8, 10, 12)
    except Exception as e:
        assert False, f"pizza_inches crashed with {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_split_bill_no_crash(s):
    """Verify that split_bill does not crash on arbitrary text, invalid
    delimiters, non-numeric values, division by zero, or None."""
    try:
        result = split_bill(s)
        assert isinstance(result, (int, float))
        assert result >= 0.0
    except Exception as e:
        assert False, f"split_bill crashed with {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# Additional Property-Based Tests: Valid Functionality & Boundary Properties
# ---------------------------------------------------------------------------

@given(st.lists(st.sampled_from(["cheese", "olives", "onion", "paneer"]), max_size=10))
def test_toppings_price_valid_combinations(toppings_list):
    """Verify that toppings_price accurately totals valid toppings combinations."""
    csv_text = ",".join(toppings_list)
    price_map = {"cheese": 40, "olives": 30, "onion": 20, "paneer": 50}
    expected = sum(price_map[t] for t in toppings_list)
    assert toppings_price(csv_text) == expected


@given(st.sampled_from(["S", "M", "L", "s", "m", "l"]))
def test_pizza_inches_valid_sizes(size):
    """Verify that pizza_inches maps standard pizza sizes case-insensitively."""
    size_map = {"S": 8, "M": 10, "L": 12}
    assert pizza_inches(size) == size_map[size.strip().upper()]


@given(st.integers(min_value=1, max_value=100000), st.integers(min_value=1, max_value=100))
def test_split_bill_valid_division(total, people):
    """Verify that split_bill calculates per-person share correctly for valid totals."""
    text = f"{total}/{people}"
    assert split_bill(text) == round(total / people, 2)


@given(st.one_of(st.integers(), st.floats(), st.booleans(), st.lists(st.text())))
def test_defensive_type_handling(non_str_val):
    """Verify that functions gracefully handle non-string data types without crashing."""
    assert toppings_price(non_str_val) == 0
    assert pizza_inches(non_str_val) == 0
    assert split_bill(non_str_val) == 0.0
