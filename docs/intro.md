# Welcome to the Sphinx-CLI-Recorder documentation!

```{warning}
The library is in its early stages!
```

This Sphinx extension is a tool to allow you to easily automate terminal/CLI recording sessions (without you having to leave your editor 🤯)

Suppose you are developing a neat CLI application, possibly with [rich](rich:introduction) (get it?) visual output. In that case, you put blood, sweat, and tears into the development part but do you want to put the same amount of effort into the documentation?
Shouldn't it be easy to show what your CLI application can do?
If you record a terminal session to show-case how to interact with your tool, you need to ensure that the recording is kept up-to-date and doesn't break with future updates.
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
