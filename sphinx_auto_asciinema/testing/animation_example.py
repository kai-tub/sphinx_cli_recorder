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
        '''def loop_last(values: Iterable[T]) -> Iterable[Tuple[bool, T]]:
    """Iterate and generate a tuple with a flag for last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    for value in iter_values:
        yield False, previous_value
        previous_value = value
    yield True, previous_value''',
        "python",
        line_numbers=True,
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
    if Confirm.ask("Do you want to see a cool prompt?"):
        progress_example()
    else:
        print(Panel("Ok... :pleading_face:\n\n\nBye :hand:", expand=False))


if __name__ == "__main__":
    main()
