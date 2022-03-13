(security)=
# Security concerns

:::{note} TL;DR
- The directive will execute arbitrary code
- Pull-request/changes to the documentation may not be reviewed as much in-depth as code changes
  - Could lead to issues if used in large/complex code-bases that want to show-case _dangerous_ operations
- Possible solution would be to add _whitelist_ support
:::

Please be aware of potential security issues this library may introduce.
The command within the directive will be run as a subprocess.
If the command includes malicious code, it will be executed!
There is no command _validation_.
You should always think twice about using commands like `rm` within the documentation!

To put the security issues that may be caused by this extension in relation to other scenarios:
Calling a CLI command could also run malicious code _behind_ the scenes and _could_ be merged into a project by not closely inspecting the changes to the code.
Installing a Python package may also execute arbitrary code.

I am trying to raise awareness of potential attacks because I believe that code is checked in more detail in contrast to changes to the documentation.
I _assume_ that a code reviewer will most probably catch a _malicious_ `subprocess` command within the code but may not double-check changes to these directives.

## Solution
_A_ possible solution could be to only execute commands that are whitelisted.
The idea is to provide a CLI tool that can be used to generate the whitelist file dynamically.
A potential reviewer only has to inspect a single file to check what commands could be executed.

Theoretically, one could extend the CI to check if the whitelist file is up-to-date and fail if this is not the case.
But I think a single whitelist file that can be automatically updated is a good middle-ground that would help reviewers avoid missing potentially dangerous code from within the documentation.

A global configuration file that lives **outside** of the directory could be used to configure arbitrary code execution.
This would allow developers that create new documentation or are updating the documentation to not _think_ about the whitelist file and only generate it at the end, possible with a `precommit` hook.
