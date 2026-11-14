"""
Lab 7: Fuzz Testing for Input Validation Bugs
Hardened Implementation of hotel_booking.py
Defensive programming applied to prevent crashes from malformed, unexpected, or null inputs.
"""

def nights_stayed(days):
    """
    Calculate the number of nights stayed between check-in and check-out days.
    Input format expected: 'check_in-check_out' (e.g. '12-15' -> 3).
    Hardened against: None, non-string, missing hyphen, non-numeric values, negative duration.
    """
    if not isinstance(days, str):
        return None
    try:
        parts = days.split('-')
        if len(parts) != 2:
            return None
        check_in_str, check_out_str = parts[0].strip(), parts[1].strip()
        if not check_in_str or not check_out_str:
            return None
        check_in = int(check_in_str)
        check_out = int(check_out_str)
        if check_out < check_in:
            return None
        return check_out - check_in
    except (ValueError, TypeError, AttributeError):
        return None


def room_floor(room_code):
    """
    Extract the floor number from a room code.
    Input format expected: 'Building-FloorRoom' (e.g. 'D-305' -> 3).
    Hardened against: None, non-string, missing hyphen, empty number, non-digit floor prefix.
    """
    if not isinstance(room_code, str):
        return None
    try:
        parts = room_code.split('-')
        if len(parts) < 2:
            return None
        number = parts[1].strip()
        if not number or not number[0].isdigit():
            return None
        return int(number[0])
    except (ValueError, TypeError, IndexError, AttributeError):
        return None


def booking_label(names_csv):
    """
    Format a guest list CSV into a booking label with the lead guest capitalized
    and the count of additional guests.
    Input format expected: 'ravi, priya' -> 'Ravi +1'.
    Hardened against: None, non-string, empty strings, spaces only, trailing commas.
    """
    if not isinstance(names_csv, str):
        return ""
    try:
        names = [n.strip() for n in names_csv.split(',') if n.strip()]
        if not names:
            return ""
        lead = names[0]
        lead_formatted = lead.capitalize() if lead else ""
        additional_count = max(0, len(names) - 1)
        return f"{lead_formatted} +{additional_count}"
    except (ValueError, TypeError, IndexError, AttributeError):
        return ""


def main():
    print("==== Running nights_stayed ====")
    user_input = input("Enter check-in and check-out day (e.g. 12-15): ")
    result = nights_stayed(user_input)
    print("Nights:", result)

    print("\n==== Running room_floor ====")
    user_input = input("Enter a room code (e.g. D-305): ")
    result = room_floor(user_input)
    print("Floor:", result)

    print("\n==== Running booking_label ====")
    user_input = input("Enter guest names as CSV (e.g. ravi, priya): ")
    result = booking_label(user_input)
    print("Booking Label:", result)


if __name__ == "__main__":
    main()
