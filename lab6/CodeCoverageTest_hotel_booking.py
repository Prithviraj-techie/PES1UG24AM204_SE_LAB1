import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# -------------------------------------------------------------
# Test Suite for Statement / Line Coverage (Target: 100%)
# -------------------------------------------------------------

def test_booking_cost_valid_standard():
    """Test standard room regular booking without peak or extra guests."""
    assert booking_cost("standard", 2, 2, False) == 4000


def test_booking_cost_unknown_room():
    """Verify ValueError is raised for an unknown room type."""
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("penthouse", 2, 2, False)


def test_booking_cost_invalid_nights():
    """Verify ValueError is raised when nights < 1."""
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 2, False)


def test_booking_cost_peak_season_and_extra_guests_and_long_stay():
    """Test peak season surcharge, extra guests fee, and long stay discount together."""
    # deluxe rate = 3500; peak rate = 3500 + 3500 // 4 = 4375
    # total for 7 nights = 4375 * 7 = 30625
    # 3 guests (1 extra) = (3 - 2) * 500 * 7 = 3500 -> total = 34125
    # 7 nights discount (10%) = 34125 - 34125 // 10 = 34125 - 3412 = 30713
    assert booking_cost("deluxe", 7, 3, True) == 30713


def test_booking_cost_suite_short_stay():
    """Test suite calculation for a short stay."""
    assert booking_cost("suite", 3, 2, False) == 18000


def test_cancellation_refund_full():
    """Test 100% refund when cancelled 7 or more days before."""
    assert cancellation_refund(1000, 10, False) == 1000


def test_cancellation_refund_moderate_days_member():
    """Test 50% refund plus 25% member bonus when cancelled 2-6 days before."""
    # 500 + 250 = 750
    assert cancellation_refund(1000, 4, True) == 750


def test_cancellation_refund_late_member():
    """Test 0% base refund plus 25% member bonus when cancelled < 2 days before."""
    # 0 + 250 = 250
    assert cancellation_refund(1000, 1, True) == 250


def test_room_upgrade_no_free_rooms():
    """Test that room remains unchanged when no rooms are free."""
    assert room_upgrade("standard", True, 0) == "standard"


def test_room_upgrade_standard_to_deluxe_member():
    """Test member upgrade from standard to deluxe."""
    assert room_upgrade("standard", True, 3) == "deluxe"


def test_room_upgrade_deluxe_to_suite_member():
    """Test member upgrade from deluxe to suite."""
    assert room_upgrade("deluxe", True, 3) == "suite"


def test_room_upgrade_suite_member():
    """Test member already having suite remains suite."""
    assert room_upgrade("suite", True, 3) == "suite"
