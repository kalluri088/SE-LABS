"""Pizza Order Application - Hardened with Input Validation.

Software Engineering Lab 7: Fuzz Testing with Hypothesis
Student Name: Kalluri Yaswanth
SRN: PES2UG24CS212
Assigned Application: pizza_order.py (L6_L7_24_pizza_order)
"""

TOPPINGS = {"cheese": 40, "olives": 30, "onion": 20, "paneer": 50}
SIZES = {"S": 8, "M": 10, "L": 12}


def toppings_price(toppings_csv):
    """Calculate the total price of requested toppings from a comma-separated string.
    
    Hardened against:
    - NoneType and non-string inputs (returns 0)
    - Empty strings and whitespace-only items (returns 0)
    - Unrecognized/unknown toppings (safely skipped, no KeyError)
    - Trailing or leading commas
    """
    if not isinstance(toppings_csv, str):
        return 0
    total = 0
    for t in toppings_csv.split(","):
        topping = t.strip().lower()
        if topping in TOPPINGS:
            total += TOPPINGS[topping]
    return total


def pizza_inches(size):
    """Return the diameter in inches for a standard pizza size (S, M, L).
    
    Hardened against:
    - NoneType and non-string inputs (returns 0)
    - Empty strings and whitespace (returns 0)
    - Unknown/invalid size designations (returns 0 instead of KeyError)
    - Mixed case inputs (normalized via upper())
    """
    if not isinstance(size, str):
        return 0
    key = size.strip().upper()
    return SIZES.get(key, 0)


def split_bill(text):
    """Split the total bill among the specified number of people formatted as 'total/people'.
    
    Hardened against:
    - NoneType and non-string inputs (returns 0.0)
    - Malformed strings without '/' or with multiple '/' (returns 0.0)
    - Non-numeric total or people values (returns 0.0 instead of ValueError)
    - Division by zero (people == 0 returns 0.0 instead of ZeroDivisionError)
    - Negative values for total or people (returns 0.0)
    """
    if not isinstance(text, str):
        return 0.0
    parts = text.split("/")
    if len(parts) != 2:
        return 0.0
    try:
        total = float(parts[0].strip())
        people = float(parts[1].strip())
        if people <= 0 or total < 0:
            return 0.0
        return round(total / people, 2)
    except (ValueError, ZeroDivisionError, OverflowError):
        return 0.0


def main():
    print("==== Running toppings_price ====")
    user_input = input("Enter toppings as CSV (e.g. cheese,olives): ")
    result = toppings_price(user_input)
    print("Toppings Price:", result)

    print("\n==== Running pizza_inches ====")
    user_input = input("Enter pizza size (S/M/L): ")
    result = pizza_inches(user_input)
    print("Size in Inches:", result)

    print("\n==== Running split_bill ====")
    user_input = input("Enter total and people (e.g. 900/3): ")
    result = split_bill(user_input)
    print("Per Person:", result)


if __name__ == "__main__":
    main()
