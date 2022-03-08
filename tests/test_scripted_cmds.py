from pydantic import ValidationError
import pytest
import pexpect
from sphinx_cli_recorder.scripted_cmds import (
    SleepTimes,
    scripted_cmd_interaction,
    timed_cmd_interaction,
)
import sys

PEXPECT_TYPE = pexpect.pty_spawn.spawn


@pytest.fixture
def simple_prompt_proc() -> PEXPECT_TYPE:
    return pexpect.spawn("python -m sphinx_cli_recorder.testing.prompt", timeout=1)


@pytest.fixture
def simple_prompt_proc_with_echo() -> PEXPECT_TYPE:
    # Doesn't work as expected
    return pexpect.spawn(
        "python -m sphinx_cli_recorder.testing.prompt",
        logfile=sys.stdout,
        encoding="utf-8",
        timeout=1,
    )


@pytest.mark.asyncio
async def test_scripted_cmd_interaction_no_path(simple_prompt_proc: PEXPECT_TYPE):
    expects = [":"]
    sends = ["n"]
    await scripted_cmd_interaction(simple_prompt_proc, expects, sends)
    # test if command has executed
    await simple_prompt_proc.expect(pexpect.EOF, timeout=1, async_=True)
    assert simple_prompt_proc.exitstatus == 0


@pytest.mark.asyncio
async def test_scripted_cmd_interaction_yes_path(simple_prompt_proc: PEXPECT_TYPE):
    expects = [":", ":", ":"]
    sends = ["y", "2", "husky"]
    await scripted_cmd_interaction(simple_prompt_proc, expects, sends)
    # test if command has executed
    await simple_prompt_proc.expect(pexpect.EOF, timeout=1, async_=True)
    assert simple_prompt_proc.exitstatus == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["expects", "sends", "sleep_times"],
    [
        (":", ["n"], SleepTimes()),
        (":::", ["n"], SleepTimes()),
        ([":"], "n", SleepTimes()),
        ([":"], ["n"], 0.1),
    ],
)
async def test_scripted_cmd_interaction_wrong_input(
    simple_prompt_proc: PEXPECT_TYPE, expects, sends, sleep_times
):
    with pytest.raises(ValidationError):
        await scripted_cmd_interaction(simple_prompt_proc, expects, sends, sleep_times)


@pytest.mark.asyncio
async def test_scripted_cmd_interaction_wrong_cmd_input():
    no_proc = "ls"
    with pytest.raises(ValidationError):
        await scripted_cmd_interaction(no_proc, [":"], ["b"])


@pytest.mark.asyncio
async def test_timed_cmd_interaction_no_path(simple_prompt_proc: PEXPECT_TYPE):
    sends = ["n"]
    await timed_cmd_interaction(simple_prompt_proc, sends)
    # test if command has executed
    await simple_prompt_proc.expect(pexpect.EOF, timeout=1, async_=True)
    assert simple_prompt_proc.exitstatus == 0


@pytest.mark.asyncio
async def test_timed_cmd_interaction_yes_path(simple_prompt_proc: PEXPECT_TYPE):
    sends = ["y", "2", "husky"]
    await timed_cmd_interaction(simple_prompt_proc, sends)
    # test if command has executed
    await simple_prompt_proc.expect(pexpect.EOF, timeout=1, async_=True)
    assert simple_prompt_proc.exitstatus == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["sends", "sleep_times"],
    [
        ("nnn", SleepTimes()),
        (["n"], 0.1),
    ],
)
async def test_timed_cmd_interaction_wrong_input(
    simple_prompt_proc: PEXPECT_TYPE, sends, sleep_times
):
    with pytest.raises(ValidationError):
        await timed_cmd_interaction(simple_prompt_proc, sends, sleep_times)


@pytest.mark.asyncio
async def test_timed_cmd_interaction_wrong_cmd_input():
    no_proc = "ls"
    with pytest.raises(ValidationError):
        await timed_cmd_interaction(no_proc, [":"], ["b"])
