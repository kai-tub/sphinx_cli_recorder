# Sphinx Auto Asciinema

## How does it work?

Please note that the project is in a _very_ early stage, the way the extension works _will_ change in the future.

Currently, the Sphinx extension is a wrapper around the awesome terminal
recorder asciinema.
<!-- continue about asciinema -->
To automate the interaction with asciinema, `pexpect` is used.
A long-term goal would be to upstream the _scripting_ functionality to asciinema.

## Security concerns

Please be aware of potential security issues this library may introduce.
The command within the directive will be run as a subprocess.
If the command includes malicious code, it will be executed!
There is no command _validation_.
You should always think twice about using commands like `rm` within the documentation.

To put the security issues that may be caused by this extension in relation to other scenarios:

Calling a CLI command could also run malicious code _behind_ the scenes and _could_ be merged into a project by not closely inspecting the changes to the code.
Installing a Python package may also execute arbitrary code.

The reason why I am trying to raise awareness of potential attacks is that I believe that code is checked in more detail in contrast to changes to the documentation.
I _assume_ that a code reviewer will most probably catch a _malicious_ `subprocess` command within the code, but may not double-check changes to these directives.

A future plan is to only execute commands that are whitelisted.
The idea is to provide a CLI tool that can be used to generate the whitelist file dynamically.
A potential reviewer than only has to inspect a single file to check what commands could be executed.

Theoretically one could extend the CI to check if the whitelist file is up-to-date and fail if this is not the case.
Trying to reduce the likelihood of _automatically_ updating the whitelist file without checking.
But I think a single white-list file that can be automatically updated is a good middle-ground that would help reviewers not to miss potentially dangerous code from within the documentation.

A global configuration file that lives **outside** of the directory could be used to configure arbitrary code execution.
As well as configuring the input to the command.
