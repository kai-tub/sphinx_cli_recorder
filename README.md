# Sphinx Auto Asciinema

Before releasing I would like to have:
- Almost complete test-coverage
- A nice looking documentation page with ethical ads
  - Furo?
- The command-wait specification
  - This should also include multi-line inputs

## Command-Wait specification
To provide a convenient way to interact with command-prompts,
the Directive must provide a way to specify the inputs for the command prompts.
The extension should allow to easily automate the different scenarios.

A terminal specific _issue_ is that there is no way to know that the terminal is
_waiting_ for an input.

expect.exact

TODO: Run in unicode mode

Would prefer TOML but will use yaml arrays, because popular alternative
to RST-Sphinx is MyST and that uses yaml-frontmatter to set parameters.

### Alternative specification
For easier use I could also implement a execute-wait style loop.
It would be:
- Easier to use
  - User only has to provide input
  - User does not need to know/understand that colors are combined generated with escape sequences
  - Less confusing YAML
- No deterministic behavior
  - Time between commands could be long enough on dev-machine, but too slow on CI
  - _Sudden_ break in doc-pipeline due to longer execute time
  - Issues would be way harder to find
  - For complex interactions, there output must be stored to allow the user to see at _which stage_ the program has failed



## Potential issues

Not really checking the read/write buffer.
Could easily overflow.
Colors are not trimmed from the output.
So expecting a colored character set will probably not work.

I don't think that it is necessary to have an individual settings for the terminals.
The width and height should be applied globally.
The replay speed may be set globally.


## Roadmap

I personally would really like to have an interactive shell session, such that the
command that will be executed is _typed_ into a shell to make it clear how the command was executed.
As there could be a difference between the command within the directive and the explanation around the directive.
But this is not at all trivial:
1. It introduces a dependency to an external shell which may produce different visual results depending on the configuration
2. Waiting for the shell prompt is hard, because one may not be able to tell how the prompt is configured
3. It is hard to tell when the _relevant_ command is done with execution.
   1. The shell prompt characters could easily be included in the interative command loop

Possible direction would be to look back at the `pyexpect.reprloop` and see if it is possible to check for returncodes.

It might not be worth it to go down this path in the early stages of this library.
A possible work-around would be to investigate how to highlight the asciinema _title_.

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
