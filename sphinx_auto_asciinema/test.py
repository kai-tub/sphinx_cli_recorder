"""
A very simple interactive prompt.
Only useful for testing.
"""
if __name__ == "__main__":
    answer = input("Do you want to go through the prompt? [y/n]:")
    if "y" in answer.lower():
        fruit = input("Name your favorite fruit:")
        print(fruit)
    else:
        print("No")
