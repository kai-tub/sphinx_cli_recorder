# Sphinx Auto Asciinema

Before releasing I would like to have:
- Almost complete test-coverage
- A nice looking documentation page with ethical ads
  - Furo (doesn't work currently)

## Current issues:
Global settings are not applied; I think this is also discussed inside of the furo theme

## Command-Wait specification
To provide a convenient way to interact with command-prompts,
the Directive must provide a way to specify the inputs for the command prompts.
The extension should allow to easily automate the different scenarios.

A terminal specific _issue_ is that there is no way to know that the terminal is
_waiting_ for an input.

expect.exact

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
