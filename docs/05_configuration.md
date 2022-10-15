(Configuration)=
# Configuration

## Recorder Configuration
### Columns
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.asciinema_player_settings.AsciinemaRecorderSettings.cols
```

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
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.asciinema_player_settings.AsciinemaRecorderSettings.rows
```

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

## Player Configuration

### Auto-Play
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.asciinema_player_settings.AsciinemaPlayerSettings.autoplay
```

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
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.asciinema_player_settings.AsciinemaPlayerSettings.preload
```

### Loop
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.asciinema_player_settings.AsciinemaPlayerSettings.loop
```

::::{dropdown} :loop: 3
:animate: fade-in-slide-down

:::{record_timed_cli_interaction} python -m sphinx_cli_recorder.testing.tiny_prompt
:rows: 10
:loop: 3

    - "y"
:::
::::

### Start-At
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.asciinema_player_settings.AsciinemaPlayerSettings.startat
```

### Speed
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.asciinema_player_settings.AsciinemaPlayerSettings.speed

```

### Idle Time Limit
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.asciinema_player_settings.AsciinemaRecorderSettings.idletimelimit

```

### Fit
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.asciinema_player_settings.AsciinemaPlayerSettings.fit

```

### Poster
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.asciinema_player_settings.AsciinemaPlayerSettings.poster

```
::::{dropdown} :poster: "data:text/plain,rich --help"
:animate: fade-in-slide-down

:::{record_cli_cmd} rich --help
:autoplay: "false"
:poster: "data:text/plain,rich --help"
:rows: 67
:::
::::

::::{dropdown} :poster: "rich --help"
:animate: fade-in-slide-down

:::{record_cli_cmd} rich --help
:autoplay: "false"
:poster: "rich --help"
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

```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.asciinema_player_settings.AsciinemaPlayerSettings.theme

```

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

## Scripted Interaction Configuration

(between-characters)=
### Between Characters
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.scripted_cmds.SleepTimes.between_character

```

(between-commands)=
### Between Commands
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.scripted_cmds.SleepTimes.between_commands

```

(before-close)=
### Before Close
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.scripted_cmds.SleepTimes.before_close

```

(timeout)=
### Timeout
```{eval-rst}
.. autopydantic_field:: sphinx_cli_recorder.scripted_cmds.SleepTimes.timeout

```
