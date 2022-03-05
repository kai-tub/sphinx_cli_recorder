import asyncio
import shutil
import tempfile
from pathlib import Path
from typing import List, Optional, Sequence

import asyncer
import pexpect
import pexpect.replwrap
from icecream import ic
from pydantic import validate_arguments

from sphinx_auto_asciinema.scripted_cmds import (
    SleepTimes,
    scripted_cmd_interaction,
    timed_cmd_interaction,
)


@validate_arguments()
async def scripted_asciicast_runner(
    cmd: str,
    expects: Optional[Sequence[str]],
    sends: Optional[Sequence[str]],
    output_fp: Path,
    sleep_time: SleepTimes,
):
    with tempfile.NamedTemporaryFile() as tmpfile:
        proc = pexpect.spawn(
            f"asciinema rec --stdin --command='{cmd}' --quiet --overwrite {tmpfile.name}"
        )
        ic("after proc init")
        if expects is not None:
            await scripted_cmd_interaction(proc, expects, sends, sleep_time)
        else:
            if sends is not None:
                await timed_cmd_interaction(proc, sends, sleep_time)
            else:
                ic("Waiting for command to stop")
        await asyncio.sleep(sleep_time.after_command)
        # wait for last command to exit
        await proc.expect(pexpect.EOF, timeout=sleep_time.timeout, async_=True)
        shutil.copy2(tmpfile.name, output_fp)


@validate_arguments
async def scripted_asciicasts_runner(
    cmds: List[str],
    expect_groups: Sequence[Optional[Sequence[str]]],
    send_groups: Sequence[Optional[Sequence[str]]],
    output_fps: Sequence[Path],
    sleep_time: SleepTimes,
):
    async with asyncer.create_task_group() as task_group:
        for cmd, expects, sends, output_fp in zip(
            cmds,
            expect_groups,
            send_groups,
            output_fps,
        ):
            ic()
            task_group.soonify(scripted_asciicast_runner)(
                cmd, expects, sends, output_fp, sleep_time
            )


# commands = [
#     "python -m rich.prompt",
#     "python -m rich.prompt",
#     "python -m rich.panel",
# ]

# expects_sends = (
#     (":", "y"),
#     (":", "11"),
#     (":", "1"),
#     (":", "abcdefg"),
#     (":", "per"),
#     (":", "pear"),
# )

# expects, sends = zip(*expects_sends)
# expect_groups = (expects, None, None)
# sends_groups = (sends, sends, None)
# ic(sends)

# asyncer.syncify(scripted_cmds_runner, raise_sync_error=False)(
#     cmds=commands,
#     expect_groups=expect_groups,
#     send_groups=sends_groups,
#     output_fps=["0.rec", "1.rec", "panel.rec"],
#     sleep_time=SleepTimes(),
# )
