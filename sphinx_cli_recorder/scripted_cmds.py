import asyncio
from typing import Sequence

import pexpect  # type: ignore
from pydantic import BaseSettings, NonNegativeFloat, validate_arguments
from typing_extensions import TypeAlias

PEXPECT_TYPE: TypeAlias = pexpect.pty_spawn.spawn


class Config:
    arbitrary_types_allowed = True


class SleepTimes(BaseSettings):
    """
    Collection of various timing options.
    """

    between_character: NonNegativeFloat = 0.1
    between_commands: NonNegativeFloat = 1.0
    after_command: NonNegativeFloat = 1.0
    timeout: NonNegativeFloat = 30


@validate_arguments(config=Config)
async def _send_to_proc(proc: PEXPECT_TYPE, send: str, sleep_times: SleepTimes):
    await asyncio.sleep(sleep_times.between_commands)
    for char in send:
        proc.send(char)
        await asyncio.sleep(sleep_times.between_character)
    proc.sendline()


@validate_arguments(config=Config)
async def scripted_cmd_interaction(
    proc: PEXPECT_TYPE,
    expects: Sequence[str],
    sends: Sequence[str],
    sleep_times: SleepTimes = SleepTimes(),
):
    expects, sends = list(expects), list(sends)
    if len(expects) != len(sends):
        raise ValueError(
            "The `expects` and `sends` sequences have to have the same length!"
        )

    for expect, send in zip(expects, sends):
        await proc.expect_exact(expect, async_=True)
        await _send_to_proc(proc, send, sleep_times)


@validate_arguments(config=Config)
async def timed_cmd_interaction(
    proc: PEXPECT_TYPE,
    sends: Sequence[str],
    sleep_times: SleepTimes = SleepTimes(),
):
    for send in sends:
        await _send_to_proc(proc, send, sleep_times)
