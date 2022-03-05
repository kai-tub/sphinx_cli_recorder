import pytest
from sphinx_auto_asciinema.asciinema_block_parser import *


# Future: Let Hypthesis loose on the content input!
def test_scripted_cmd_interaction_parser_simple():
    content = """\
    - [first, ":::"]
    - [second, "'"]
    - [third, "?"]
    """
    wait_for_send_pairs = scripted_cmd_interaction_parser(content)
    assert [p.wait_for for p in wait_for_send_pairs] == ["first", "second", "third"]
    assert [p.send for p in wait_for_send_pairs] == [":::", "'", "?"]


def test_scripted_cmd_interaction_parser_yml():
    content = """\
    -
        - first
        - ":::"
    -
        - second
        - "'"
    -
        - third
        - "?"
    """
    wait_for_send_pairs = scripted_cmd_interaction_parser(content)
    assert [p.wait_for for p in wait_for_send_pairs] == ["first", "second", "third"]
    assert [p.send for p in wait_for_send_pairs] == [":::", "'", "?"]


def test_scripted_cmd_interaction_parser_invalid():
    content = """
    - [first, ":::"]
    - [second, "'"]
    - [third, "?", "extra"]
    """
    with pytest.raises(ValueError):
        scripted_cmd_interaction_parser(content)


def test_timed_cmd_interaction_parser_simple():
    content = """\
    - "first_input"
    - second
    - 'third'
    """
    send_strings = timed_cmd_interaction_parser(content)
    assert [s.send for s in send_strings] == ["first_input", "second", "third"]


def test_timed_cmd_interaction_parser_yml():
    content = """\
    ["first_input", "second", 'third']
    """
    send_strings = timed_cmd_interaction_parser(content)
    assert [s.send for s in send_strings] == ["first_input", "second", "third"]


def test_timed_cmd_interaction_parser_invalid():
    content = """
    - [first, ":::"]
    """
    with pytest.raises(ValueError):
        timed_cmd_interaction_parser(content)
