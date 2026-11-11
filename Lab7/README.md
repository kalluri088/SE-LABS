# Software Engineering Lab 7: Fuzz Testing for Input Validation Bugs

**Student:** Kalluri Yaswanth  
**SRN:** PES2UG24CS212  
**Course:** Software Engineering (UE22CS341AA)  
**Assigned Repository:** [`SETAPESU26/L6_L7_24_pizza_order`](https://github.com/SETAPESU26/L6_L7_24_pizza_order)  
**Application Module:** `pizza_order.py` (Handout generic: `processor.py`)  
**Test Module:** `test_pizza_order.py` (Handout generic: `test_processor.py`)  
**Environment:** Omarchy Linux (Arch Linux x86_64), Python 3.14.8, `pytest 9.2.0`, `hypothesis 6.170.15`

---

## Deliverables & File Inventory

| File | Description |
|------|-------------|
| `pizza_order.py` | Defensively hardened application with full input validation |
| `test_pizza_order.py` | Completed Hypothesis property-based fuzz test suite (7 passed test cases) |
| `stage1_original_app.png` | Terminal screenshot of original unhardened application execution |
| `stage2_failing_hypothesis.png` | Terminal screenshot of Hypothesis fuzz tests exposing unhandled crashes |
| `stage3_fixed_app.png` | Terminal screenshot of hardened application executing valid inputs |
| `stage4_passing_hypothesis.png` | Terminal screenshot of Hypothesis fuzz test suite passing 100% |
| `PES2UG24CS212_SE_Lab7_Report.pdf` | Comprehensive black-and-white laboratory report adhering to course rubric |
| `Lab_7_FuzzTesting_Student_Handout.pdf` | Official laboratory student handout |

---

## Verification Commands

Activate the Python environment and run tests:

```bash
# Run the hardened application interactively:
python pizza_order.py

# Execute the property-based fuzz test suite with Hypothesis:
pytest test_pizza_order.py -v
```
