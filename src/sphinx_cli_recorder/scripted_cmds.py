import asyncio
from typing import Sequence

import pexpect  # type: ignore
from pydantic import BaseSettings, Field, NonNegativeFloat, validate_arguments
from typing_extensions import TypeAlias

PEXPECT_TYPE: TypeAlias = pexpect.pty_spawn.spawn


class Config:
    arbitrary_types_allowed = True


class SleepTimes(BaseSettings):
    """
    Collection of various timing options.
    """

    between_character: NonNegativeFloat = Field(
        default=0.1,
        description="""\
            The time to wait between each character in seconds.

            By default 0.1s
        """,
    )
    between_commands: NonNegativeFloat = Field(
        default=1.0,
        description="""\
            The time to wait between sending _commands_
            (and before the first) in seconds.

            By default 1.0s
        """,
    )
    before_close: NonNegativeFloat = Field(
        default=1.0,
        description="""\
            The time to wait after sending the last command
            in seconds.
            This translates to how long the final output
            should be shown before stopping the stream.

            By default 1.0s
        """,
    )
    timeout: NonNegativeFloat = Field(
        default=30,
        description="""\
            The time to wait before interrupting to
            wait for an output from the terminal and
            to raise an exception.
            This timeout is used for both the plain and
            the interactive command runner.
        """,
    )


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
