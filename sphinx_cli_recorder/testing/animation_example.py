"""
A very simple interactive prompt.
Only useful for testing.
"""

import time

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.prompt import Confirm, Prompt
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table


def progress_example():
    syntax = Syntax(
        '''def hello_potential_user():
    """Say hello to a potential user 💜"""
    # this is comment
    s = "Hello hard-worker"
    print(s)''',
        "python",
    )

    progress_renderables = [
        "This is a cool CLI application you want to show to the 🌍",
        Panel("Which probably includes some [i][blue]neat visualizations[/]"),
        "Like styling some source-code",
        syntax,
        Rule(),
        "But you should [b]not[/b] have to record and host it manually!",
        "You've worked enough writing the CLI application",
        "Automate the recording and hosting with:",
        Panel("[magenta]Sphinx-CLI-Recorder[/]"),
        Rule("Thank you for watching until the end!"),
    ]

    console = Console(record=True)

    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:

        task = progress.add_task("[green]Processing", total=len(progress_renderables))

        for renderable in progress_renderables:
            time.sleep(1.5)
            progress.log(renderable)
            progress.update(task, advance=1)
        time.sleep(1)


def main():
    # name = Prompt.ask("Do you want to see a cool prompt? [y/n]:")
    progress_example()
    # if Confirm.ask("Do you want to see a cool prompt?"):
    #     progress_example()
    # else:
    #     print(Panel("Ok... :pleading_face:\n\n\nBye :hand:", expand=False))


if __name__ == "__main__":
    main()
