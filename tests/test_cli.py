import pytest

from assistant.cli.bot import parse_input


def test_parse_simple_command():
    command, args = parse_input("hello")

    assert command == "hello"
    assert args == []


def test_parse_command_with_quoted_name():
    command, args = parse_input(
        'add "Ivan Petrenko" 0671234567'
    )

    assert command == "add"
    assert args == ["Ivan Petrenko", "0671234567"]


def test_parse_note_with_quotes():
    command, args = parse_input(
        'add-note "Python project meeting"'
    )

    assert command == "add-note"
    assert args == ["Python project meeting"]


def test_parse_empty_input():
    command, args = parse_input("")

    assert command == ""
    assert args == []


def test_parse_command_case_insensitive():
    command, args = parse_input("HELLO")

    assert command == "hello"
    assert args == []


def test_parse_unclosed_quotes():
    with pytest.raises(ValueError):
        parse_input('add "Ivan Petrenko 0671234567')
