# Internals

This library builds on the sholders of two giants.
- [asciinema](https://github.com/asciinema/asciinema)
- [pexpect](pexpect:index)

## Asciinema
Currently, the Sphinx extension is a wrapper around the awesome terminal recorder asciinema.

### Recorder
A couple of words on the recorder

### Player
A couple of words on the player

## Pexpect
To automate the interaction with asciinema, `pexpect` is used.

- Why no windows
- What other limitations


## Architecture

:::{warning}
The project is in a _very_ early stage, the way the extension works _will_ change in the future.
:::

- Directive/node parsing
- Async loop
