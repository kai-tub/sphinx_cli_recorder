import pty
from unsync import unsync
import anyio
from asyncer import syncify
import os

# from time import sleep
import asyncio
import fastcore.all as fc
import pexpect
import pexpect.replwrap

shell = "/bin/sh"


def test_pty():
    # in both read cases an empty bytestring refers to end of file
    with open("tmp", "wb") as script:

        # hooks into the output of the shell and reads everything
        # not only what is returned but everything that is seen on screen
        # So the "session" that is being recorded
        def master_read(fd):
            data = os.read(fd, 1024)
            script.write(data)
            return data

        # stdin_read is passed file descriptor 0, to read from the parent process’s standard input.
        # this would allow me to modify/transform the stdin but not to program the input itself...

        script.write("This is the start\n".encode())
        pty.spawn(shell, master_read)
        script.write("This is the end\n".encode())


# I should re-think what I want
# I "only" want to pass small chunks to the input
# And maybe send some more after some time


def test_pexpect():
    child = pexpect.spawn("asciinema rec --stdin --overwrite test.rec")
    print("after child")
    # child = pexpect.spawn("/bin/sh")
    # regular expression!
    child.expect("$")
    child.sendline("echo 1")
    child.expect("1")


# repl = pexpect.replwrap.bash()
# theoretically works as expected
# repl = pexpect.replwrap.REPLWrapper("/bin/sh", "$ ", None)
# repl.run_command("echo 1 >> tmp")

# --quiet is necessary to ensure that nothing matches with the output of asciinema!
# sleeping is necessary to ensure that the output is readable
# Could easily create my own loop to configure the sleep between character inputs
# And the sleep between commands
# By default the normal expect should be used
# The
# child = pexpect.spawn(

expects_sends = (
    (":", "y"),
    (":", "11"),
    (":", "1"),
    (":", "abcdefg"),
    (":", "per"),
    (":", "pear"),
)

# works very well!
# the next thing would probably be to run this async in sphinx to
# run the programs in parallel

# The main issue is that the colored output cannot be correctly parsed...
# Of course these include the terminal color information and _could_ potentially be stripped? Somehow?
# But this has a low-priority and is not necessary for the initial implementation

# It would probably be more important to work on the Sphinx Directive options
# And possibly decide on the 'command language'


# might want to move to anyio to have typing support...
# @unsync
async def scripted_cmd_interaction(
    proc,
    expects_sends,
    chr_sleep_time: float = 0.2,
    trans_sleep_time: float = 1.0,
):
    for expect, send in expects_sends:
        proc.expect_exact(expect)
        for chr in send:
            proc.send(chr)
            await asyncio.sleep(chr_sleep_time)
        proc.sendline()
        await asyncio.sleep(trans_sleep_time)
    proc.sendeof()


@fc.delegates(scripted_cmd_interaction)
async def scripted_cmd_runner(cmd, expects_sends, **kwargs):
    proc = pexpect.spawn(
        f"asciinema rec --stdin --command='{cmd}' -q --overwrite zzz.rec"
    )
    if expects_sends is not None:
        await scripted_cmd_interaction(proc, expects_sends, **kwargs)


@fc.delegates(scripted_cmd_runner)
async def multi_scripted_cmd_runner(cmds, expects_sends, **kwargs):
    for cmd, exps_sends in zip(cmds, expects_sends):
        await scripted_cmd_runner(cmd, exps_sends, **kwargs)


commands = [
    "python -m rich.prompt",
    "python -m rich.prompt",
]
exps_sends = [expects_sends, expects_sends]

syncify(multi_scripted_cmd_runner, raise_sync_error=False)(
    cmds=commands, expects_sends=exps_sends
)

# unfutures = []
# for cmd, exp_sends in commands:
# res = [u.result() for u in unfutures]


# def test_popen():
# child = PopenSpawn("/bin/sh")
# child.sendline("asciinema rec --stdin --overwrite test.rec")
# child = PopenSpawn("asciinema rec --command='/bin/sh' --stdin --overwrite test.rec")
# child.expect_exact("$ ")


# child = pexpect.spawn("/bin/sh")
# child.sendline("echo 1")
# child.expect("1")
# # print("Saw 1")
# child.sendeof()
