import time
from datetime import datetime
from enum import Enum
from typing import Counter, Optional, Union

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt, conint, validator


class AsciinemaTheme(str, Enum):
    """Pre-defined asciinema themes"""

    asciinema = "asciinema"
    monokai = "monokai"
    tango = "tango"
    solarized_dark = "solarized-dark"
    solarized_light = "solarized-light"


class AsciinemaFit(str, Enum):
    width = "width"
    height = "height"
    both = "both"
    none = "none"


# The options will be converted to lower in the Directive options class
# To keep it consistent I will also use the same style.
# I don't know why, but the options javascript <script> tag from asciinema
# doesn't care if it is lower/upper case
# Future: Use alias functionality to keep the code pythonic and still
# make it obvious in JS/HTML code
class AsciinemaRecorderSettings(BaseModel):
    """Asciinema Recorder Settings"""

    rows: PositiveInt = Field(
        default=20,
        description="""\
            Define the number of rows the terminal should have.
            The extension will ensure that the same number of rows is used for the recording and playback.
            If the number of rows is too low, the beginning of the output may be lost.
            Similar to how a _real_ terminal behaves.""",
    )
    cols: PositiveInt = Field(
        default=80,
        description="""\
            Define the number of columns the terminal should have.
            The extension will ensure that the same number of columns is used for the recording and playback.
            If the number of columns is too low, the output could be wrapped weirdly.
            The text will also be zoomed-in to fit the width of the container.""",
    )
    idletimelimit: PositiveFloat = Field(
        default=5,
        description="""\
            Limit recorded terminal inactivity to max <idletimelimit> seconds.
            *Not* milli-seconds!""",
    )


class AsciinemaPlayerSettings(AsciinemaRecorderSettings):
    autoplay: bool = Field(
        default=False,
        description="""\
            Set if the playback should start automatically.
            If `True` the player will start even if the video is *not* in the viewport!
            By default, the playback has to be started manually.

            Possible reasons to enable auto-play is to showcase some rich help-text of a command, where the full output is shown by tuning the number of _rows_ to display.
            Another reason is to start an eye-catching animation at the top of the page.""",
    )
    preload: bool = Field(
        default=False,
        description="""\
            Set this option to true if the recording should be preloaded on player's initialization.
        """,
    )
    loop: Union[bool, PositiveInt] = Field(
        default=False,
        description="""\
            If set to `True` video will loop indefinitely.
            When set to a number, then the recording will be re-played `loop` times and stopped
            after that.

            The number of loops will only be respected in the "first" playback.
            Please note that the recording will *immediately* restart once it has
            finished. If there is no wait-time after finishing the loop, it will
            look like no output has been generated since the next loop will
            "repaint" the window.
        """,
    )
    # First try to coerce to Integer than Str
    startat: Union[conint(ge=0, strict=True), str] = 0
    # could also be int
    speed: PositiveFloat = 1.0
    theme: AsciinemaTheme = AsciinemaTheme.asciinema
    # FUTURE: could use poster to show what command
    # was run/will be run
    poster: Optional[str] = None
    fit: AsciinemaFit = AsciinemaFit.width
    fontsize: str = "small"

    @validator("startat")
    def startat_match(cls, v):
        if isinstance(v, int):
            print(v)
            return v
        if isinstance(v, str):
            counts = Counter(v)
            if counts[":"] == 0:
                # corner-case: silently try to convert as last-hail marry
                return int(v)
            elif counts[":"] == 1:
                tm = time.strptime(v, "%H:%M")
                return time.strftime("%H:%M", tm)
            elif counts[":"] == 2:
                tm = time.strptime(v, "%H:%M:%S")
                return time.strftime("%H:%M:%S", tm)
            raise ValueError(f"{v} is an unknown time-format!")
        raise TypeError(f"{v} of type {type(v)} is an unsupported startat type!")
