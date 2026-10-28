import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# =====================================================================
# Branch Coverage Test Suite (Target: 100% Branch & Statement Coverage)
# Covers every branch (True and False) and decision condition path
# =====================================================================

# ---------------------------------------------------------------------
# 1. Tests for booking_cost decision branches
# ---------------------------------------------------------------------

def test_booking_cost_unknown_room_branch():
    """Branch: room not in ROOM_RATE (True)."""
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("presidential", 2, 2, False)


def test_booking_cost_invalid_nights_branch():
    """Branch: room in ROOM_RATE (False), nights < 1 (True)."""
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 2, False)


def test_booking_cost_no_peak_no_extra_no_long_stay():
    """
    Branch coverage:
    - room not in ROOM_RATE: False
    - nights < 1: False
    - is_peak_season: False
    - guests > 2: False (guests == 2)
    - nights >= 7: False (nights == 6)
    """
    # standard = 2000 * 6 = 12000
    assert booking_cost("standard", 6, 2, False) == 12000


def test_booking_cost_peak_extra_guests_long_stay():
    """
    Branch coverage:
    - is_peak_season: True
    - guests > 2: True (guests == 4)
    - nights >= 7: True (nights == 7)
    """
    # deluxe rate = 3500; peak rate = 3500 + 3500 // 4 = 4375
    # total base = 4375 * 7 = 30625
    # extra guests = (4 - 2) * 500 * 7 = 7000 -> 37625
    # 7 nights discount (10%) = 37625 - 37625 // 10 = 37625 - 3762 = 33863
    assert booking_cost("deluxe", 7, 4, True) == 33863


def test_booking_cost_suite_single_guest_regular():
    """Branch coverage: room == 'suite', guests == 1 (guests <= 2)."""
    # suite = 6000 * 3 = 18000
    assert booking_cost("suite", 3, 1, False) == 18000


# ---------------------------------------------------------------------
# 2. Tests for cancellation_refund decision branches
# ---------------------------------------------------------------------

def test_cancellation_refund_7_or_more_days():
    """Branch: days_before >= 7 (True) -> 100% refund immediately."""
    assert cancellation_refund(1000, 7, False) == 1000
    assert cancellation_refund(1000, 14, True) == 1000


def test_cancellation_refund_between_2_and_6_days_non_member():
    """
    Branch coverage:
    - days_before >= 7: False
    - days_before >= 2: True
    - is_member: False
    Refund = 50%
    """
    assert cancellation_refund(1000, 3, False) == 500


def test_cancellation_refund_between_2_and_6_days_member():
    """
    Branch coverage:
    - days_before >= 7: False
    - days_before >= 2: True
    - is_member: True
    Refund = 50% + 25% = 75%
    """
    assert cancellation_refund(1000, 2, True) == 750


def test_cancellation_refund_less_than_2_days_non_member():
    """
    Branch coverage:
    - days_before >= 7: False
    - days_before >= 2: False
    - is_member: False
    Refund = 0%
    """
    assert cancellation_refund(1000, 1, False) == 0


def test_cancellation_refund_less_than_2_days_member():
    """
    Branch coverage:
    - days_before >= 7: False
    - days_before >= 2: False
    - is_member: True
    Refund = 0 + 25% = 250
    """
    assert cancellation_refund(1000, 0, True) == 250


# ---------------------------------------------------------------------
# 3. Tests for room_upgrade decision branches
# ---------------------------------------------------------------------

def test_room_upgrade_rooms_free_is_zero():
    """Branch: rooms_free == 0 (True) -> returns current room."""
    assert room_upgrade("standard", True, 0) == "standard"
    assert room_upgrade("deluxe", False, 0) == "deluxe"


def test_room_upgrade_standard_member_free_rooms():
    """Branch: rooms_free > 0, room == 'standard' and is_member (True)."""
    assert room_upgrade("standard", True, 5) == "deluxe"


def test_room_upgrade_standard_non_member():
    """Branch: rooms_free > 0, room == 'standard' is True but is_member is False."""
    assert room_upgrade("standard", False, 5) == "standard"


def test_room_upgrade_deluxe_member_free_rooms():
    """Branch: rooms_free > 0, room == 'deluxe' and is_member (True)."""
    assert room_upgrade("deluxe", True, 5) == "suite"


def test_room_upgrade_deluxe_non_member():
    """Branch: rooms_free > 0, room == 'deluxe' is True but is_member is False."""
    assert room_upgrade("deluxe", False, 5) == "deluxe"


def test_room_upgrade_suite_member():
    """Branch: rooms_free > 0, room == 'suite', falls through to return room."""
    assert room_upgrade("suite", True, 5) == "suite"


def test_room_upgrade_suite_non_member():
    """Branch: rooms_free > 0, room == 'suite', non-member."""
    assert room_upgrade("suite", False, 5) == "suite"
