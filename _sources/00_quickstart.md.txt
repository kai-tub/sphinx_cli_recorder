# Quickstart

The best way to understand what the extension is capable of and if it is helpful for you, is to simply look at an example:

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


The extension embeds a _recording_ of the provided command into your documentation:
```bash
python -m sphinx_cli_recorder.testing.animation_example
```

Showcasing an example output of a specific command is especially helpful for tools similar to  [rich](rich:introduction) that provide fantastic formatting/highlighting options for the command line.
The directive can automatically generate a nice-looking and always up-to-date help page for a CLI tool in development.

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

```{record_cli_cmd} rich --help
:rows: 67
:autoplay: "True"
```

But the extension is not limited to executing commands!
It is also possible to walk through command prompts and script the interaction. 🤯

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
The previous method, `record_timed_cli_interaction`, relies on _waiting_ before sending input strings to the terminal.
A different method, `record_scripted_cli_interaction`, is to _wait_ until a specific character or sequences of characters have been received from the terminal to send the _input_:

:::::{tab-set}
::::{tab-item} reST
:sync: reST

:::{code-block} reST
.. record_scripted_cli_interaction:: python -m sphinx_cli_recorder.testing.prompt

    - [":", "y"]
    - [":", "5"]
    - [":", "2"]
    - [":", "poodle"]
    - [":", "husky"]
:::

::::

::::{tab-item} md
:sync: md

:::{code-block} md
```{record_scripted_cli_interaction} python -m sphinx_cli_recorder.testing.prompt

    - [":", "y"]
    - [":", "5"]
    - [":", "2"]
    - [":", "poodle"]
    - [":", "husky"]
```
::::
:::::

<!-- Doesn't make the option in lower! -->
```{record_scripted_cli_interaction} python -m sphinx_cli_recorder.testing.prompt

    - [":", "y"]
    - [":", "5"]
    - [":", "2"]
    - [":", "poodle"]
    - [":", "husky"]
```

## Runner directives
This sphinx extension provides three directives to record the execution of, or the interaction with, a CLI application.
You may use the following flowchart to decide which directive you should use.

```{mermaid} mermaid_files/decision.mmd
```

Please take a look at the [](Usage) section for more details (otherwise this shouldn't be called a _Quickstart_ section, I guess 🤔)
