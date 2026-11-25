"""Decorators for command handlers (from homework 05)."""

from functools import wraps


def input_error(func):
    """Turn input errors into friendly messages instead of crashing."""

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error) or "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name."

    return inner
