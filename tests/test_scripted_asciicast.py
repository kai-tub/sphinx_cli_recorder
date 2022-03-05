# TODO:

# validate asciinema recording file by inspecting it with asciinema
# and ensuring that more than 1 frame is present


# TODO: check that total duration is close to sleep_times!

import pytest
import tempfile
from sphinx_auto_asciinema.scripted_asciicast_runner import (
    scripted_asciicast_runner,
    scripted_asciicasts_runner,
)
from sphinx_auto_asciinema.scripted_cmds import SleepTimes
from pathlib import Path


@pytest.mark.asyncio
async def test_single_cmd():
    cmd = "python --version"
    expects = None
    sends = None
    with tempfile.NamedTemporaryFile() as tmpfile:
        await scripted_asciicast_runner(cmd, expects, sends, tmpfile.name, SleepTimes())
        assert Path(tmpfile.name).stat().st_size > 0
