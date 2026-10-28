# Lab 6: Code and Branch Coverage Analysis

## Student Details
- **Repository:** PES1UG24AM204_SE_LAB1
- **Module Under Test:** `hotel_booking.py`
- **Application Scope:** Hotel booking pricing, season/guest surcharges, cancellation refunds, and room upgrades.

---

## 1. Objective & Learning Outcomes
- Understand the fundamental differences between **Line Coverage** and **Branch Coverage**.
- Use Python's `coverage` tool and `pytest` framework to measure, analyze, and maximize test coverage.
- Identify untested decision branches and design targeted test suites to reach **100% Code Coverage** and **100% Branch Coverage** (>90% requirement).

---

## 2. Tested Application Overview (`hotel_booking.py`)

The application consists of three core business logic functions:
1. `booking_cost(room, nights, guests, is_peak_season)`:
   - Validates room type against `ROOM_RATE` dictionary (`standard`: 2000, `deluxe`: 3500, `suite`: 6000).
   - Validates minimum duration (`nights >= 1`).
   - Surcharges +25% during peak season (`rate += rate // 4`).
   - Surcharges extra guests above 2 at 500/night/guest.
   - Applies a 10% discount for extended stays (`nights >= 7`).
2. `cancellation_refund(amount, days_before, is_member)`:
   - 7+ days prior: 100% full refund (`refund = amount`).
   - 2 to 6 days prior: 50% base refund (`amount // 2`).
   - < 2 days prior: 0% base refund.
   - Member perk: Adds +25% of amount bonus refund (`amount // 4`) for cancellations under 7 days.
3. `room_upgrade(room, is_member, rooms_free)`:
   - If `rooms_free == 0`: No upgrade (returns original room).
   - If member and `standard`: Upgrades to `deluxe`.
   - If member and `deluxe`: Upgrades to `suite`.
   - Otherwise: Returns original room.

---

## 3. Coverage Analysis: Line Coverage vs. Branch Coverage

| Metric | Starter Test Cases | Code Coverage Test (`CodeCoverageTest_hotel_booking.py`) | Branch Coverage Test (`BranchCoverageTest_hotel_booking.py`) |
| :--- | :--- | :--- | :--- |
| **Total Statements** | 32 | 32 | 32 |
| **Missed Statements** | 18 | **0** | **0** |
| **Line Coverage** | 44% | **100%** | **100%** |
| **Total Branches** | 22 | 22 | 22 |
| **Missed Branches** | 6 partial / 14 untested | 1 partial | **0** |
| **Branch Coverage** | 37% | 98% | **100%** |
| **Test Status** | 2 passed | 12 passed | **17 passed** |

### Key Concept: Why 100% Line Coverage $\neq$ 100% Branch Coverage
- **Line Coverage** checks whether every physical line of code was executed at least once. In `CodeCoverageTest_hotel_booking.py`, we executed all 32 statements, reaching 100% line coverage.
- However, branch coverage exposed that certain conditions were only tested for `True` and never `False` (e.g. testing `is_member == True` when `days_before < 7` executed line 28, but the `False` branch jumping directly to line 29 was untracked).
- `BranchCoverageTest_hotel_booking.py` exercises both `True` and `False` outcomes for every conditional branch, achieving a flawless **100% Branch Coverage**.

---

## 4. Test Suite Structure & Branch Decision Matrix

### Decision Branches Covered:
1. `room not in ROOM_RATE`:
   - `True`: `test_booking_cost_unknown_room_branch` (raises `ValueError`)
   - `False`: valid room types (`standard`, `deluxe`, `suite`)
2. `nights < 1`:
   - `True`: `test_booking_cost_invalid_nights_branch` (raises `ValueError`)
   - `False`: valid nights ($\ge 1$)
3. `is_peak_season`:
   - `True`: `test_booking_cost_peak_extra_guests_long_stay` (+25% rate)
   - `False`: `test_booking_cost_no_peak_no_extra_no_long_stay`
4. `guests > 2`:
   - `True`: `test_booking_cost_peak_extra_guests_long_stay` (`guests = 4`)
   - `False`: `test_booking_cost_no_peak_no_extra_no_long_stay` (`guests = 2`)
5. `nights >= 7`:
   - `True`: `test_booking_cost_peak_extra_guests_long_stay` (`nights = 7`, 10% discount)
   - `False`: `test_booking_cost_no_peak_no_extra_no_long_stay` (`nights = 6`)
6. `days_before >= 7`:
   - `True`: `test_cancellation_refund_7_or_more_days` (100% refund)
   - `False`: `days_before < 7`
7. `elif days_before >= 2`:
   - `True`: `test_cancellation_refund_between_2_and_6_days_non_member` (50% refund)
   - `False`: `test_cancellation_refund_less_than_2_days_non_member` (0% refund)
8. `if is_member` (when `days_before < 7`):
   - `True` with `days_before >= 2`: `test_cancellation_refund_between_2_and_6_days_member` (75% refund)
   - `False` with `days_before >= 2`: `test_cancellation_refund_between_2_and_6_days_non_member` (50% refund)
   - `True` with `days_before < 2`: `test_cancellation_refund_less_than_2_days_member` (25% refund)
   - `False` with `days_before < 2`: `test_cancellation_refund_less_than_2_days_non_member` (0% refund)
9. `if rooms_free == 0`:
   - `True`: `test_room_upgrade_rooms_free_is_zero` (returns unchanged room)
   - `False`: `rooms_free > 0`
10. `room == "standard" and is_member`:
    - `True`: `test_room_upgrade_standard_member_free_rooms` (upgrades to deluxe)
    - `False` (standard, non-member): `test_room_upgrade_standard_non_member` (stays standard)
11. `elif room == "deluxe" and is_member`:
    - `True`: `test_room_upgrade_deluxe_member_free_rooms` (upgrades to suite)
    - `False` (deluxe, non-member): `test_room_upgrade_deluxe_non_member` (stays deluxe)
12. Fallthrough (`suite` or non-upgradeable):
    - `test_room_upgrade_suite_member` (suite stays suite)
    - `test_room_upgrade_suite_non_member` (suite stays suite)

---

## 5. Verification Commands

To reproduce the coverage reports:

```bash
# Line Coverage Analysis
coverage erase
coverage run -m pytest CodeCoverageTest_hotel_booking.py
coverage report -m

# Branch Coverage Analysis
coverage erase
coverage run --branch -m pytest BranchCoverageTest_hotel_booking.py
coverage report -m
```

---

## 6. Deliverable Screenshots
Terminal output screenshots are stored in `lab6/screenshots/`:
- `screenshots/line_coverage_screenshot.jpg`: Terminal output demonstrating **100% Statement/Line Coverage**.
- `screenshots/branch_coverage_screenshot.jpg`: Terminal output demonstrating **100% Branch Coverage**.
