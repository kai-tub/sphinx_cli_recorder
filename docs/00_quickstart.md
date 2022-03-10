# Quickstart

- [ ] Explain with mermaid the three different execution modes
- [ ] Show minimal example to run a single command
- [ ] Show a minimal example to run through a timed-prompt
- [ ] Show a minimal example to run through a scripted wait-run prompt
- [ ] Point out the major difference

The best way to understand what the extension is capable of and if it is useful for you, is to simply look at an example:

<!-- Future: Ensure that correct command is always run -->



:::::{tab-set}
::::{tab-item} reST
:sync: reST

:::{code-block} reST
.. record_cli_cmd:: python -m sphinx_cli_recorder.testing.animation_example
:::

::::

::::{tab-item} md
:sync: md

:::{code-block} md
```{record_cli_cmd} python -m sphinx_cli_recorder.testing.animation_example
```
::::
:::::

<!-- Doesn't make the option in lower! -->
```{record_cli_cmd} python -m sphinx_cli_recorder.testing.animation_example
```


The extension embeds a _recording_ of a command, here:
```bash
python -m sphinx_cli_recorder.testing.animation_example
```

Showcasing an example output of a specific command is especially helpful for tools similar to  [rich](rich:introduction) that provide amazing formatting/highlighting options for the command line.
The directive can be used to automatically generate a nice-looking and always up-to-date help page for a CLI tool in development.

:::::{tab-set}
::::{tab-item} reST
:sync: reST

:::{code-block} reST
.. record_cli_cmd:: rich --help
:::

::::

::::{tab-item} md
:sync: md

:::{code-block} md
```{record_cli_cmd} rich --help
```
::::
:::::

<!-- Doesn't make the option in lower -->
```{record_cli_cmd} rich --help
:rows: 67
:autoplay: "True"
```
But the extension is not limited to executing commands!
It is also possible to walk through command-prompts and to script the interaction. 🤯

:::::{tab-set}
::::{tab-item} reST
:sync: reST

:::{code-block} reST
.. record_timed_cli_interaction:: python -m sphinx_cli_recorder.testing.prompt

    - "y"
    - "5"
    - "2"
    - "poodle"
    - "husky"
:::

::::

::::{tab-item} md
:sync: md

:::{code-block} md
```{record_timed_cli_interaction} python -m sphinx_cli_recorder.testing.prompt

    - "y"
    - "5"
    - "2"
    - "poodle"
    - "husky"
```
::::
:::::

<!-- Doesn't make the option in lower! -->
```{record_timed_cli_interaction} python -m sphinx_cli_recorder.testing.prompt

    - "y"
    - "5"
    - "2"
    - "poodle"
    - "husky"
```

The interactive functionality targets library authors of CLI tools and command prompt authors.


## Installation
Install the package:
```
pip install sphinx-cli-recorder
```

Then add the extension to your [sphinx config (config.py)](sphinx:extensions)

```python
extensions = [
    "sphinx-cli-recorder"
]
```


## Runner directives
This sphinx extension provides three directives to animate a CLI interaction.
To decide which directive you should use, you may use the following flow-chart.

```{mermaid}
    flowchart TD
        Command --> B{Interaction\nRequired?}
        B -- No --> C[Use cmd_runner]
        B -- Yes --> D[Use timed/scripted_cmd_runner]
```

## Command runner
The command runner will simply execute the input `command` as a new process.
The command must terminate without any input.



## Timed command runner

Has a list of strings that will be send to the terminal.
The `send` string will be terminated by appending a newline, or from a users viewpoint, by _hitting enter_.
Between all `sends` (and before the first) the `between_commands` time in seconds
is waited.
To create more _realistic_ command inputs, the characters of the `send` strings will be send
with a delay.
After each character, the sending is paused for `between_character` seconds.

## Scripted command runner


For more details on the directives and on how to configure the options, please
see the following section.
