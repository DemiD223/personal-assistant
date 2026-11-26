"""Decorators for command handlers (from homework 05)."""

from functools import wraps


def input_error(func):
    """Turn input errors into friendly messages instead of crashing."""
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error) or "Invalid input."
        except KeyError as error:
            return error.args[0] if error.args else "Not found."
        except IndexError:
            return "Not enough arguments."
    return inner
