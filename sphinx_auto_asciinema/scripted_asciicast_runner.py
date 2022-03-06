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
from sphinx_auto_asciinema.asciinema_player_settings import AsciinemaRecorderSettings

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
    recorder_settings: AsciinemaRecorderSettings,
):
    with tempfile.NamedTemporaryFile() as tmpfile:
        spawn_template = "asciinema rec --stdin --command='{cmd}' --rows={rows} --cols={cols} --idle-time-limit={idletimelimit} --quiet --overwrite {fp}"
        spawn_cmd = spawn_template.format(
            cmd=cmd,
            rows=recorder_settings.rows,
            cols=recorder_settings.cols,
            idletimelimit=recorder_settings.idletimelimit,
            fp=tmpfile.name,
        )

        # spawn_cmd =
        proc = pexpect.spawn(spawn_cmd)
        if expects is not None:
            await scripted_cmd_interaction(proc, expects, sends, sleep_time)
        else:
            if sends is not None:
                await timed_cmd_interaction(proc, sends, sleep_time)
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
    sleep_times_groups: Sequence[SleepTimes],
    recorder_settings_list: Sequence[AsciinemaRecorderSettings],
):
    async with asyncer.create_task_group() as task_group:
        for cmd, expects, sends, output_fp, sleep_times, recorder_settings in zip(
            cmds,
            expect_groups,
            send_groups,
            output_fps,
            sleep_times_groups,
            recorder_settings_list,
        ):
            task_group.soonify(scripted_asciicast_runner)(
                cmd, expects, sends, output_fp, sleep_times, recorder_settings
            )
