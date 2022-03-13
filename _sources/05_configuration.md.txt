(Configuration)=
# Configuration

<!-- FUTURE: use autopydantic_model -->
<!-- Or something similar to automatically generate the documentation from code -->

:::{warning}
In the dropdown menus, the last few columns are cut-off.
The issue seems to be due to a CSS conflict regarding the dropdown's alignment/width/margin properties.
If the `border` CSS is disabled in the `class=asciinema-terminal`, the issue is _fixed_, in that the end of span/line is visible, but now there is no border...

Frontend development in Sphinx makes me cry 😭
:::

```{admonition} TODO
:class: admonition-todo

Finalize the examples
```

## Recorder Configuration

## Player Configuration
### Columns
    :cols: PositiveNumber

Define the number of columns the terminal should have.
The extension will ensure that the same number of columns is used for the recording and playback.
If the number of columns is too low, the output could be wrapped weirdly.
The text will also be _zoomed-in_ to fit the width of the container.

::::{dropdown} :cols: 20
:animate: fade-in-slide-down

:::{record_cli_cmd} python -m rich.panel
:cols: 20
:::
::::

::::{dropdown} :cols: 40
:animate: fade-in-slide-down

:::{record_cli_cmd} python -m rich.panel
:cols: 40
:::
::::

### Rows
    :rows: PositiveNumber

Define the number of rows the terminal should have.
The extension will ensure that the same number of rows is used for the recording and playback.
If the number of rows is too low, the beginning of the output may be lost.
Similar to how a _real_ terminal behaves.

::::{dropdown} :rows: 5
:animate: fade-in-slide-down

:::{record_cli_cmd} python -m rich.panel
:rows: 5
:::
::::

::::{dropdown} :rows: 10
:animate: fade-in-slide-down

:::{record_cli_cmd} python -m rich.panel
:rows: 10
:::
::::

### Auto-Play
    :autoplay: "true"/"false"

Set if the playback should start automatically.
By default, the playback has to be started manually.

Possible reasons to enable auto-play is to showcase some rich help-text of a command, where the full output is shown by tuning the number of _rows_ to display.
Another reason is to start an eye-catching animation at the top of the page.

::::{dropdown} :autoplay: "false"
:animate: fade-in-slide-down

:::{record_cli_cmd} rich --help
:autoplay: "false"
:rows: 67
:::
::::

::::{dropdown} :autoplay: "true"
:animate: fade-in-slide-down

:::{record_cli_cmd} rich --help
:autoplay: "true"
:rows: 67
:::
::::

### Preload

### Loop

### Start-At

### Speed

### Idle Time Limit

### Fit

### Poster
::::{dropdown} :poster: "data:text/plain,rich --help"
:animate: fade-in-slide-down

:::{record_cli_cmd} rich --help
:autoplay: "false"
:poster: "data:text/plain,rich --help"
:rows: 67
:::
::::

::::{dropdown} :poster: "npt:0:1"
:animate: fade-in-slide-down

:::{record_cli_cmd} rich --help
:autoplay: "false"
:poster: "npt:0:1"
:rows: 67
:::
::::

### Theme
Define the style of the background and color palette of the terminal.

::::{dropdown} :theme: "asciinema"
:animate: fade-in-slide-down

:::{record_cli_cmd} rich --help
:autoplay: "true"
:theme: "asciinema"
:rows: 67
:::
::::

::::{dropdown} :theme: "monokai"
:animate: fade-in-slide-down

:::{record_cli_cmd} rich --help
:autoplay: "true"
:theme: "monokai"
:rows: 67
:::
::::

::::{dropdown} :theme: "tango"
:animate: fade-in-slide-down

:::{record_cli_cmd} rich --help
:autoplay: "true"
:theme: "tango"
:rows: 67
:::
::::

::::{dropdown} :theme: "solarized-dark"
:animate: fade-in-slide-down

:::{record_cli_cmd} rich --help
:autoplay: "true"
:theme: "solarized-dark"
:rows: 67
:::
::::

::::{dropdown} :theme: "solarized-light"
:animate: fade-in-slide-down

:::{record_cli_cmd} rich --help
:autoplay: "true"
:theme: "solarized-light"
:rows: 67
:::
::::
