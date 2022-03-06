# Roadmap

- [ ] Increase test coverage
  - [ ] Better test the option validators
  - [ ] Add integration tests to test the sphinx-code
- [ ] Try to convince other maintainers to use this extension
- [ ] Add more details to the documentation

## If-I-Had-Unlimited-Time
I personally would really like to have an interactive shell session, such that the
command that will be executed is _typed_ into a shell to make it clear how the command was executed.
As there could be a difference between the command within the directive and the explanation around the directive.
But this is not at all trivial:
1. It introduces a dependency to an external shell which may produce different visual results depending on the configuration
2. Waiting for the shell prompt is hard, because one may not be able to tell how the prompt is configured
3. It is hard to tell when the _relevant_ command is done with execution.
   1. The shell prompt characters could easily be included in the interative command loop

Possible direction would be to look back at the `pyexpect.reprloop` and see if it is possible to check for returncodes.

It might not be worth it to go down this path in the early stages of this library.
A possible work-around would be to investigate how to use the `poster` option of asciinema to display the command-to-run before.

Also on the _nice-to-have-but-might-never-happen-list_:
- [ ] whitelist option
- [ ] mixed await and time specification
- [ ] add better error-messages
- [ ] add aliases to the validators for the mixedCase option-inputs
