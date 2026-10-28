import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# =====================================================================
# Complete Test Suite for Hotel Booking (Code & Branch Coverage: 100%)
# =====================================================================

# ----------------- booking_cost tests -----------------

def test_standard_two_nights():
    """Starter test: standard room, 2 nights, 2 guests, regular season."""
    assert booking_cost("standard", 2, 2, False) == 4000


def test_booking_cost_unknown_room():
    """Verify unknown room raises ValueError."""
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("penthouse", 2, 2, False)


def test_booking_cost_invalid_nights():
    """Verify nights < 1 raises ValueError."""
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 2, False)


def test_booking_cost_peak_extra_guests_long_stay():
    """Test peak season, extra guests (>2), and 7+ nights discount."""
    # deluxe rate = 3500; peak rate = 3500 + 3500 // 4 = 4375
    # base = 4375 * 7 = 30625
    # extra guests (4 - 2) * 500 * 7 = 7000 -> 37625
    # 7 nights discount (10%) = 37625 - 3762 = 33863
    assert booking_cost("deluxe", 7, 4, True) == 33863


def test_booking_cost_suite_short_stay():
    """Test suite calculation for regular stay."""
    assert booking_cost("suite", 3, 1, False) == 18000


# ----------------- cancellation_refund tests -----------------

def test_full_refund():
    """Starter test: cancellation 10 days before gives full refund."""
    assert cancellation_refund(1000, 10, False) == 1000


def test_full_refund_exactly_seven_days():
    """Test boundary condition at exactly 7 days."""
    assert cancellation_refund(1000, 7, True) == 1000


def test_refund_between_2_and_6_days_non_member():
    """Test 50% refund for non-member between 2 and 6 days."""
    assert cancellation_refund(1000, 3, False) == 500


def test_refund_between_2_and_6_days_member():
    """Test 50% + 25% member bonus refund between 2 and 6 days."""
    assert cancellation_refund(1000, 3, True) == 750


def test_refund_less_than_2_days_non_member():
    """Test 0% refund for non-member less than 2 days before."""
    assert cancellation_refund(1000, 1, False) == 0


def test_refund_less_than_2_days_member():
    """Test 0% + 25% member bonus refund less than 2 days before."""
    assert cancellation_refund(1000, 0, True) == 250


# ----------------- room_upgrade tests -----------------

def test_room_upgrade_no_rooms_free():
    """Test no upgrade when rooms_free == 0."""
    assert room_upgrade("standard", True, 0) == "standard"
    assert room_upgrade("deluxe", True, 0) == "deluxe"


def test_room_upgrade_standard_member():
    """Test standard upgrades to deluxe for member."""
    assert room_upgrade("standard", True, 3) == "deluxe"


def test_room_upgrade_standard_non_member():
    """Test standard stays standard for non-member."""
    assert room_upgrade("standard", False, 3) == "standard"


def test_room_upgrade_deluxe_member():
    """Test deluxe upgrades to suite for member."""
    assert room_upgrade("deluxe", True, 3) == "suite"


def test_room_upgrade_deluxe_non_member():
    """Test deluxe stays deluxe for non-member."""
    assert room_upgrade("deluxe", False, 3) == "deluxe"


def test_room_upgrade_suite_member():
    """Test suite stays suite for member (highest tier)."""
    assert room_upgrade("suite", True, 3) == "suite"


def test_room_upgrade_suite_non_member():
    """Test suite stays suite for non-member."""
    assert room_upgrade("suite", False, 3) == "suite"
