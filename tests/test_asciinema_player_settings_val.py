import pytest
from pydantic import ValidationError

from sphinx_cli_recorder.asciinema_player_settings import *


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
