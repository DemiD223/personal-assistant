"""Upcoming birthdays helper (from homework 03).

Developer 2 adapts it to work with AddressBook and any number of days N.
"""

from datetime import datetime, timedelta


def get_upcoming_birthdays(users, days=7):
    """Return users to congratulate within the next `days` days.

    Today is included.

    Birthdays on a weekend are moved to the next Monday.
    `users` is a list of dicts: {"name": str, "birthday": "YYYY.MM.DD"}.
    """
    today = datetime.today().date()
    upcoming = []

    for user in users:
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()

        try:
            birthday_this_year = birthday.replace(year=today.year)
        except ValueError:
            birthday_this_year = birthday.replace(
                year=today.year, month=3, day=1
            )

        if birthday_this_year < today:
            try:
                birthday_this_year = birthday.replace(year=today.year + 1)
            except ValueError:
                birthday_this_year = birthday.replace(
                    year=today.year + 1, month=3, day=1
                )

        days_until = (birthday_this_year - today).days

        if 0 <= days_until < days:
            congratulation_date = birthday_this_year
            if congratulation_date.weekday() == 5:
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6:
                congratulation_date += timedelta(days=1)

            upcoming.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime(
                    "%Y.%m.%d"
                ),
            })

    return upcoming
