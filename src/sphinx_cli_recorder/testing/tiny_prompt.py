from rich import print
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.text import Text


class MyConfirm(Confirm):
    def render_default(self, default) -> Text:
        yes, no = self.choices
        return Text(f"({yes})" if default else f"({no})", style="red")


def main():
    if MyConfirm.ask("[bold]Yes[/bold] or [italic]no[/italic]?", default=True):
        print("Nice, good to know!")
    else:
        print("Ok, then not.")


if __name__ == "__main__":
    main()
