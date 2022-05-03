import pytest
from pydantic import ValidationError

from sphinx_cli_recorder.asciinema_player_settings import *
from sphinx_cli_recorder.asciinema_player_settings import _list_enum_values_as_bullets


@pytest.mark.parametrize("v", [1, 12, 123, "12:59", "01:12:59"])
def test_startat_valid(v):
    assert AsciinemaPlayerSettings(startat=v).startat == v


def test_startat_corner_case():
    # according to the asciinema-player documentation this shouldn't be allowed
    # as the input is expected to be either in HH:MM/MM:SS as string OR directly an
    # integer
    assert AsciinemaPlayerSettings(startat="123").startat == 123


@pytest.mark.parametrize("v", ["12:59:12:00", "01:", "25:00", "01:99", 1.234])
def test_startat_invalid(v):
    with pytest.raises(ValidationError):
        AsciinemaPlayerSettings(startat=v)


def test_list_themes():
    themes_str = _list_enum_values_as_bullets(AsciinemaTheme)
    themes_list = themes_str.splitlines()
    assert len(themes_list) == 5


@pytest.mark.parametrize(
    ["v", "expected"],
    [
        ("data:text/plain,rich --help", "data:text/plain,rich --help"),
        ("rich --help", "data:text/plain,rich --help"),
        ("npt:0:1", "npt:0:1"),
        (None, None),
    ],
)
def test_poster_match_valid(v, expected):
    assert AsciinemaPlayerSettings(poster=v).poster == expected
