"""Upcoming birthdays helper (from homework 03), adapted to AddressBook."""

from datetime import date, timedelta


def _next_birthday(birthday, today):
    """Return the next birthday date from today (29.02 -> 01.03)."""
    for year in (today.year, today.year + 1):
        try:
            candidate = birthday.replace(year=year)
        except ValueError:
            candidate = date(year, 3, 1)
        if candidate >= today:
            return candidate
    return candidate


def get_upcoming_birthdays(book, days=7):
    """Return contacts to congratulate within the next `days` days.

    Today is included. Birthdays on a weekend move to the next Monday.
    Returns a list of (record, congratulation_date) tuples sorted by date.

    Examples:
        get_upcoming_birthdays(book) -> birthdays in the next 7 days
        get_upcoming_birthdays(book, 30) -> birthdays in the next 30 days
    """
    today = date.today()
    upcoming = []

    for record in book.data.values():
        if record.birthday is None:
            continue

        next_birthday = _next_birthday(record.birthday.value, today)
        if (next_birthday - today).days >= days:
            continue

        congratulation_date = next_birthday
        if congratulation_date.weekday() == 5:
            congratulation_date += timedelta(days=2)
        elif congratulation_date.weekday() == 6:
            congratulation_date += timedelta(days=1)

        upcoming.append((record, congratulation_date))

    return sorted(upcoming, key=lambda item: item[1])
