from rich import print
from rich.prompt import Confirm, IntPrompt, Prompt


def main():
    print("Sphinx-CLI-Recorder can also work with interactive CLI applications!\n\n")
    if Confirm.ask(
        "Do you want to start the [b]interactive[/b] example [i]prompt[/i]?",
        default=True,
    ):
        while True:
            result = IntPrompt.ask(
                "Enter a number between [b]1[/b] and [b]3[/b]", default=2
            )
            if result >= 1 and result <= 3:
                break
            print(":pile_of_poo: [prompt.invalid]Number must be between 1 and 3")
        print(f"number={result}")

        dog = Prompt.ask("Enter your favorite dog :dog2:", choices=["husky"])
        print(f"What a surprise! Your favorite dog is also: {dog!r}")
        print("Good taste! :+1:")
    else:
        print("[b]OK :loudly_crying_face:")


if __name__ == "__main__":
    main()
