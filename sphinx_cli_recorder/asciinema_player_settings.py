from enum import Enum
from pydantic import BaseModel, PositiveFloat, PositiveInt
from typing import Union, Optional


class AsciinemaTheme(str, Enum):
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
    rows: PositiveInt = 24
    cols: PositiveInt = 80
    idletimelimit: PositiveFloat = 5


class AsciinemaPlayerSettings(AsciinemaRecorderSettings):
    autoplay: bool = False
    preload: bool = False
    loop: Union[bool, PositiveInt] = False
    # create correct validator
    startat: Union[str, PositiveInt] = 0
    # could also be int
    speed: PositiveFloat = 1.0
    theme: AsciinemaTheme = AsciinemaTheme.asciinema
    # FUTURE: could use poster to show what command
    # was run/will be run
    poster: Optional[str] = None
    fit: AsciinemaFit = AsciinemaFit.width
    fontsize: str = "small"
