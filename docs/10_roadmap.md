# Roadmap

- [ ] Increase test coverage
  - [ ] Better test the option validators
  - [ ] Add integration tests to test the sphinx-code
- [ ] Try to convince other maintainers to use this extension
- [ ] Add more details to the documentation
- [ ] Allow caching of the recordings to reduce the wait-time
- [ ] Allow reducing the number of subprocesses
  - [ ] Ideally allow the user to manually set what commands can be run together to separate _resource-heavy_ commands
- [ ] Add detailed validators for the directive options

The _long-term roadmap_:
- [ ] mixed await and time specification
- [ ] add better error-messages
- [ ] add aliases to the validators for the `camelCase` option-inputs
- [ ] re-use recording if command with _identical_ settings was already run
- [ ] whitelist option (see security)

## If-I-Had-Unlimited-Time
I would like to have an interactive shell session, such that the command that is _typed_ into a shell to make it clear how what command was run and how.
As there could be a difference between the command within the directive and the explanation around the directive.
But this is not at all trivial:
1. It introduces a dependency to an external shell which may produce different visual results depending on the configuration
2. Waiting for the shell prompt is hard because one may not be able to tell how the prompt is configured
3. It is hard to tell when the _relevant_ command is done with execution.
   1. The shell prompt characters could easily be included in the interactive command loop

A possible direction would be to look back at the `pyexpect.reprloop` and see if it is possible to check for return codes.

It might not be worth it to go down this path in the early stages of this library.
A possible work-around would be to investigate how to use the `poster` option of `asciinema` to display the command-to-run before.
