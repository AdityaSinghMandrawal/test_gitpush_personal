"""Basic for-loop examples."""


def count_up(n: int = 5) -> None:
    """Print numbers from 0 to n-1."""
    for i in range(n):
        print(i, end=" ")
    print()


def iterate_list() -> None:
    """Loop over a list of items."""
    fruits = ["apple", "banana", "cherry"]
    for fruit in fruits:
        print(f"I like {fruit}")


def with_index() -> None:
    """Loop with both index and value."""
    colors = ["red", "green", "blue"]
    for index, color in enumerate(colors):
        print(f"{index}: {color}")


def sum_numbers(n: int = 10) -> int:
    """Sum numbers from 1 to n."""
    total = 0
    for num in range(1, n + 1):
        total += num
    return total


if __name__ == "__main__":
    print("=== count_up ===")
    count_up()

    print("\n=== iterate_list ===")
    iterate_list()

    print("\n=== with_index ===")
    with_index()

    print("\n=== sum_numbers ===")
    print(f"Sum 1..10 = {sum_numbers()}")