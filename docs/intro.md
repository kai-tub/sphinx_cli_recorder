# Welcome to the Sphinx-CLI-Recorder documentation!

This Sphinx extension is tool to allow you to easily automate terminal/CLI recording session (without you having to leave the documentation document 🤯)

If you are developing a neat CLI application, possibly with [rich](rich:introduction) (get it?) visual output, you put blood, sweat and tears into the development part but do you really want to put the same amount of effort into the documentation?
If you record a terminal session to show-case how to interact with your CLI application, you need to ensure that the recording is kept up-to-date and that it doesn't break with future updates.
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

Or you are looking for a simple way to always include the most recent help text of a tool you are developing.
```{record_cli_cmd} rich --help
:rows: 67
:autoplay: "True"
```

In all cases, it is probably easier to let the _Sphinx-CLI-Recorder_ handle it for you.
It uses [asciinema](asciinema.org), a text-based terminal recorder under the hood.
Utilizing a text-based terminal player has the following advantages:
- ✅ The output is _lossless_; no more pixelated videos/images with compression artefacts
- ✅ No need to wait for huge-video files to be downloaded
- ✅ The terminal's content can be copied to the clip-board, no need to manually re-type the commands that are shown in a GIF/video

The extension helps you to automate the recording session, keeps the files up-to-date, and includes the recordings into your documentation.
The recordings will be done in parallel to minimize the documentation build time and will ensure that provided commands work, before the documentation pipeline succesffully finishes.
