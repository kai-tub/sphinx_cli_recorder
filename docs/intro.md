(welcome)=
# Welcome to the Sphinx-CLI-Recorder documentation!
[![Tests](https://img.shields.io/github/workflow/status/kai-tub/sphinx_cli_recorder/CI?color=dark-green&label=%20Tests)](https://github.com/kai-tub/sphinx_cli_recorder/actions/workflows/main.yml)
[![License](https://img.shields.io/pypi/l/sphinx_cli_recorder?color=dark-green)](https://github.com/kai-tub/sphinx_cli_recorder/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/sphinx-cli-recorder.svg)](https://pypi.org/project/sphinx-cli-recorder/)
[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=)](https://github.com/intuit/auto)

```{warning}
The library is in its early stages!
```

:::{admonition} TL;DR
:class: note

- 🎥 Record interactions (input & output) with CLI applications
- 🤖 Automate the recording process via simple Sphinx directives
- ✔️ Simple; does not require any knowledge of the underlying recording application
- ⛓️ No dependencies on external services; all files are generated and hosted locally
:::

This Sphinx extension is a tool to allow you to easily automate the recording process of CLI applications (without you having to leave your editor 🤯).

Suppose you are developing a neat CLI application, possibly with [rich](rich:introduction) (get it?) visual output. In that case, you put blood, sweat, and tears into the development part but do you want to put the same amount of effort into the documentation?
Shouldn't it be easy to show what your CLI application can do?
If you record a terminal session to show how to interact with your tool, you need to ensure that the recording is kept up-to-date and doesn't break with future updates.
Then you need to know how to upload the file and embed it into your documentation.
And all you want to do is to show something cool like:

```{record_cli_cmd} python -m sphinx_cli_recorder.testing.animation_example
:autoplay: "True"
```

Or give the user an example on how to navigate your CLI application:
```{record_timed_cli_interaction} python -m sphinx_cli_recorder.testing.prompt

    - "y"
    - "5"
    - "2"
    - "poodle"
    - "husky"
```

Or you are looking for a simple way always to include the most recent help text of a tool you are developing.
```{record_cli_cmd} rich --help
:rows: 67
:autoplay: "True"
```

In those cases, it is probably easier to let the _Sphinx-CLI-Recorder_ handle it for you. 😎
It uses [asciinema](https://asciinema.org), a text-based terminal recorder under the hood.
Utilizing a text-based terminal player has the following advantages:
- ✅ The output is _lossless_; no more pixelated videos/images with compression artifacts
- ✅ No need to wait for huge-video file downloads
- ✅ The terminal's content can be copied to the clipboard; no need to manually re-type the commands that are shown in a GIF/video

The benefits of using this Sphinx extension are:
- 🤖 Automates the recording process of [asciinema](https://asciinema.org)
- 📅 Ensures that the recordings are always up-to-date
    - 💣 If the code changes and the commands from the documentation fail, no documentation will be built
- 🏠 Keeps all of your files/data local:
    - 🔐 No need to depend on external services/tokens to upload the recordings
- 🚅 The recordings are done in parallel to minimize the documentation build time
- ☑️ Simple; no need to understand how [asciinema](https://asciinema.org) works
