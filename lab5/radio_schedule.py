"""Manage a simple radio station programme schedule."""

import sqlite3


class RadioSchedule:
    """Store programme slots and provide basic schedule operations."""

    def __init__(self):
        """Create an in-memory database for programme slots."""
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute(
            """CREATE TABLE slots (
                id INTEGER PRIMARY KEY,
                show TEXT NOT NULL,
                host TEXT NOT NULL,
                start_hour INTEGER NOT NULL,
                minutes INTEGER NOT NULL
            )"""
        )

    def add_slot(self, show, host, start_hour, minutes):
        """Add a programme slot after validating its time and details."""
        if not show.strip() or not host.strip():
            raise ValueError("Show and host names must not be empty.")
        if not 0 <= start_hour <= 23:
            raise ValueError("Start hour must be between 0 and 23.")
        if minutes <= 0 or start_hour * 60 + minutes > 24 * 60:
            raise ValueError("Duration must be positive and end by midnight.")

        self.connection.execute(
            """INSERT INTO slots (show, host, start_hour, minutes)
               VALUES (?, ?, ?, ?)""",
            (show, host, start_hour, minutes),
        )
        self.connection.commit()

    @staticmethod
    def slot_label(show, host):
        """Return a readable label for a programme and its host."""
        return f"{show} hosted by {host}"

    @staticmethod
    def overlap_free(start_hour, minutes, other_start_hour, other_minutes):
        """Return True when two programme intervals do not overlap."""
        start = start_hour * 60
        end = start + minutes
        other_start = other_start_hour * 60
        other_end = other_start + other_minutes
        return end <= other_start or other_end <= start

    def morning_shows(self):
        """Return programme names scheduled to start before noon."""
        rows = self.connection.execute(
            "SELECT show FROM slots WHERE start_hour < ? ORDER BY start_hour",
            (12,),
        )
        return [row[0] for row in rows]

    def remove_slot(self, slot_id):
        """Remove a programme slot by its database identifier."""
        self.connection.execute("DELETE FROM slots WHERE id = ?", (slot_id,))
        self.connection.commit()

    def close(self):
        """Close the database connection."""
        self.connection.close()


def main():
    """Run a short demonstration of the schedule operations."""
    schedule = RadioSchedule()
    try:
        schedule.add_slot("Sunrise Beats", "Vik", 7, 60)
        schedule.add_slot("Midday Talk", "Anu", 13, 45)
        print(schedule.slot_label("Sunrise Beats", "Vik"))
        print(
            schedule.overlap_free(7, 60, 13, 45),
            schedule.morning_shows(),
        )
        schedule.remove_slot(2)
    finally:
        schedule.close()


if __name__ == "__main__":
    main()
