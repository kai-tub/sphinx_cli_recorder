"""
A very simple interactive prompt.
Only useful for testing.
"""

import time
from rich import print
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.table import Table
from rich.panel import Panel
from rich.rule import Rule
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.console import Console


def progress_example():
    syntax = Syntax(
        '''def hello_potential_user():
    """Say hello to a potential user 💜"""
    # this is comment
    s = "Do you want to use a cool extension?"
    print(s)''',
        "python",
    )

    table = Table("rich", "is", "awesome")
    table.add_row("yes", "yep", "definitely")

    progress_renderables = [
        "This is a cool prompt",
        Panel("Aren't [i]I[/i] right?"),
        "See this nice looking [magenta]table[/]",
        table,
        "And showing some syntax...",
        syntax,
        Rule("Thank you for your patience!"),
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
