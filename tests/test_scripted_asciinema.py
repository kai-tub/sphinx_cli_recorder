# TODO:
# validate asciinema recording file by inspecting it with asciinema
# and ensuring that more than 1 frame is present


# TODO: check that total duration is close to sleep_times!

import tempfile
from pathlib import Path

import pytest

from sphinx_cli_recorder.scripted_asciinema_runner import scripted_asciinema_runner
from sphinx_cli_recorder.scripted_cmds import SleepTimes


@pytest.mark.asyncio
async def test_single_cmd(tmpdir):
    cmd = "python --version"
    expects = None
    sends = None
    p = tmpdir / "tmpfile"
    await scripted_asciinema_runner(cmd, expects, sends, p, SleepTimes())
    assert Path(p).stat().st_size > 0


@pytest.mark.asyncio
async def test_invalid_expect_send_specification(tmpdir):
    cmd = "python --version"
    expects = [":"]
    sends = None
    p = tmpdir / "tmpfile"
    # is actually catched in underlying scripted_cmds code
    with pytest.raises(
        ValueError, match="Missing `sequence` for given `expects` sequence"
    ):
        await scripted_asciinema_runner(cmd, expects, sends, p, SleepTimes())
