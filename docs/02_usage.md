(Usage)=
# Usage

The Sphinx-CLI-Recorder extension supports two kinds of _execution-modes_:
- The [_plain_ command runner](command_runner)
    - The [directive](sphinx:rst-directives) name is `record_cli_cmd`
    - The command will be run and the output logged
    - No user-input required
- An [_interactive_ command runner](interactive-runner)
    - The [directives](sphinx:rst-directives) are called:
      - `record_timed_cli_interaction`
      - `record_scripted_cli_interaction`
    - The command will be run and the output logged
    - User-input is required and it necessary to provide _steps_ to walk through the application

Or, if you are like me and would rather like to look at a picture:
```{mermaid} mermaid_files/decision.mmd
```

(command_runner)=
## Command runner
Here is a short list of the key takeaways:
- The [directive](sphinx:rst-directives) is called `record_cli_cmd`
- The command must _terminate_ without any input
    - The command is spawned as a subprocess and must terminate on its own
- The input command may contain any number of characters/whitespaces
    - _But_ no newlines are allowed

The directive syntax looks as follows:
:::::{tab-set}
::::{tab-item} reST
:sync: reST

:::{code-block} reST
. record_cli_cmd:: <CMD_TO_RUN>
:<OPTION_KEY>: <OPTION_VALUE>
:::

::::

::::{tab-item} md
:sync: md

:::{code-block} md
```{record_cli_cmd} <CMD_TO_RUN>
:<OPTION_KEY>: <OPTION_VALUE>
```
::::
:::::

Please note that the directive does **not** allow any _text-content_ after the option configuration.
There is simply no use for text input.
The provided `<CMD>` will be run as a subprocess, and since no interaction is necessary, there is no need to give any _input_.
Remember, `<CMD>` may contain any number of whitespace, so the following is allowed:

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

There are _many_ options to configure the behavior of the [directive](sphinx:rst-directives). Please refer to [](Configuration) for an extensive list with visual examples.

(interactive-runner)=
## Interactive command runner
There are two [directives](sphinx:rst-directives) that allow you to _interact_ with the command that will be run:
- [`record_timed_cli_interaction`](timed_command_runner)
- [`record_scripted_cli_interaction`](scripted_command_runner)

(timed_command_runner)=
### Timed command runner
Here is a short list of the key takeaways of the _timed_ command runner:
- The [directive](sphinx:rst-directives) is called `record_timed_cli_interaction`
- The input command may contain any number of characters/whitespaces
    - _But_ no newlines are allowed
- The command _must_ require some _input_
    - The _input_ should be provided as a list of _send_ strings enclosed by `"`
    - The _send_ string will be terminated by a newline, or from a CLI application's viewpoint, by _receiving enter_
    - The _send_ string will be sent after a configurable amount of time, **possibly not** when the terminal is ready!
- There must be a newline-character between the options and the list of strings that will be sent
- After sending the last _send_ strings, the command _must_ terminate

The _timed_ command runner has the following syntax:

:::::{tab-set}
::::{tab-item} reST
:sync: reST

:::{code-block} reST
.. record_timed_cli_interaction:: <CMD>
<OPTIONS>
<NEWLINE>
    - "<LIST>"
    - "<OF>"
    - "<SEND>"
    - "<STRINGS>"
:::

::::

::::{tab-item} md
:sync: md

:::{code-block} md
```{record_timed_cli_interaction} <CMD>
<OPTIONS>
<NEWLINE>
    - "<LIST>"
    - "<OF>"
    - "<SEND>"
    - "<STRINGS>"
```
::::
:::::

#### Drawbacks
```{warning}
The beauty of the _timed_ interactive style is that it is easy to write and reason about _but_ its simplicity comes with a cost.
```

There is no way to _know_ that a CLI application is _waiting_ for input. Instead, the next _send_ string will be sent after a specific time. If the application is _not_ ready to receive the following line yet, the recording will probably crash because the wrong input will be sent.
The time-based approach may be incredibly frustrating if the execution time differs between development machines and _works_ on one device but fails in the CI pipeline. The time to execute the command might take _too_ long for the CI systems to finish and fail documentation builds.

Another issue is that the wait time between sending the lines might become relatively long if many _sends_ are required, resulting in lengthy documentation build times.

<!-- TODO: Add timeout links -->
The main options to tune will probably be the [between-commands](between-commands) and [timeout](timeout) values.
There are _many more_ options to configure the behavior of the [directive](sphinx:rst-directives). Please refer to [](Configuration) for an extensive list with visual examples.

You made it until the end of the timed command runner documentation! 🥳
Here is a visual example output to keep you entertained:

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

```{record_timed_cli_interaction} python -m sphinx_cli_recorder.testing.prompt

    - "y"
    - "5"
    - "2"
    - "poodle"
    - "husky"
```


(scripted_command_runner)=
### Scripted command runner
Here is a short list of the key takeaways of the _scripted_ command runner:
- The [directive](sphinx:rst-directive) is called `record_scripted_cli_interaction`
- The input command may contain any number of characters/whitespaces
    - _But_ no newlines are allowed
- The command _must_ require some _expect_ and _send_ pairs
    - The inputs should be provided as a list of _expect_ and _send_ pairs, enclosed by `["<EXPECT>", "<SEND>"]`
    - After creating a subprocess with the given command, the execution will wait until the `<EXPECT>` string is received and will then continue by sending the `<SEND>` string
    - The _send_ string will be terminated by a newline, or from a CLI application's viewpoint, by _receiving enter_
- There must be a newline-character between the options and the list of strings that will be sent
- After sending the last _send_ strings, the command _must_ terminate

The _scripted_ command runner has the following syntax:

:::::{tab-set}
::::{tab-item} reST
:sync: reST

:::{code-block} reST
.. record_scripted_cli_interaction:: <CMD>
<OPTIONS>
<NEWLINE>
    - ["<EXPECT_FIRST>", "<WAIT_FIRST>"]
    - ["<EXPECT_NEXT>", "<WAIT_NEXT>"]
    - ["<EXPECT_LAST>", "<WAIT_LAST>"]
:::

::::

::::{tab-item} md
:sync: md

:::{code-block} md
```{record_timed_cli_interaction} <CMD>
<OPTIONS>
<NEWLINE>
    - ["<EXPECT_FIRST>", "<WAIT_FIRST>"]
    - ["<EXPECT_NEXT>", "<WAIT_NEXT>"]
    - ["<EXPECT_LAST>", "<WAIT_LAST>"]
```
::::
:::::

#### Drawbacks
```{warning}
The beauty of the _scipted_ interactive style is that it is _deterministic_ _but_ it is harder to read, and waiting for characters might be a lot harder than one might think.
```

There is no way to _know_ that a CLI application is _waiting_ for input. Instead, with `record_scripted_cli_interaction`, the next _send_ string will be sent after a specific string/character has been _read/received_. But this might introduce implicit limitations/issues that are hard to catch.
Let's look at the following example:

```{record_scripted_cli_interaction} python -m sphinx_cli_recorder.testing.tiny_prompt
:timeout: 1

    - ["\x1b[31m(y)\x1b[0m:", "y"]
```

It is possible to wait on `:` at the end of the prompt.
But waiting for `):` will raise a _timeout_ error.
This error is caused to how the color of the output is encoded.
In reality, the last few characters the terminal receives aren't `(y):` but `\x1b[31m(y)\x1b[0m:` 🤯.

Welcome to the world of [ANSI escape codes](https://notes.burke.libbey.me/ansi-escape-codes/).
These weird characters `\x1b[31m` are the escape sequence.
The escape sequence `\x1b[31m` tells the terminal to switch the following characters to a _red_ foreground color.
<!-- The symbol `\x1b` (ESC) defines the _start_ of an ANSI escape sequence.
The pair `\x1b[` is called the _Control Sequence Introducer_. -->
`\x1b[0m` tells the terminal to go back to the _default_ output mode, which is then followed by a _white_ colored `:` in the output.
So if we wanted to wait for the red-colored option, the directive would look like this:

:::::{tab-set}
::::{tab-item} reST
:sync: reST

:::{code-block} reST
.. record_scripted_cli_interaction:: python -m sphinx_cli_recorder.testing.tiny_prompt

    - ["\x1b[31m(y)\x1b[0m:", "y"]
:::

::::

::::{tab-item} md
:sync: md

:::{code-block} md
```{record_scripted_cli_interaction} python -m sphinx_cli_recorder.testing.tiny_prompt

    - ["\x1b[31m(y)\x1b[0m:", "y"]
```
::::
:::::

The main options to tune will probably be the [timeout](timeout) value.
There are _many more_ options to configure the behavior of the [directive](sphinx:rst-directives). Please refer to [](Configuration) for an extensive list with visual examples.
