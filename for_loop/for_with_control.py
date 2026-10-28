"""for-loops with break, continue, and else."""

from typing import List, Optional


def find_first_even(nums: List[int]) -> Optional[int]:
    """Return the first even number, or None."""
    for n in nums:
        if n % 2 == 0:
            return n
    return None


def skip_odds(nums: List[int]) -> None:
    """Print only even numbers using continue."""
    for n in nums:
        if n % 2 != 0:
            continue
        print(n, end=" ")
    print()


def stop_at_zero(nums: List[int]) -> None:
    """Print numbers until a zero appears (break)."""
    for n in nums:
        if n == 0:
            print("(stopped at 0)")
            break
        print(n, end=" ")
    print()


def search_with_else(items: List[str], target: str) -> None:
    """for-else runs when the loop does not break."""
    for item in items:
        if item == target:
            print(f"Found '{target}'")
            break
    else:
        print(f"'{target}' not found")


if __name__ == "__main__":
    sample = [1, 3, 4, 7, 8, 0, 9]

    print("=== find_first_even ===")
    print(find_first_even(sample))

    print("\n=== skip_odds ===")
    skip_odds(sample)

    print("\n=== stop_at_zero ===")
    stop_at_zero(sample)

    print("\n=== search_with_else ===")
    search_with_else(["cat", "dog", "bird"], "dog")
    search_with_else(["cat", "dog", "bird"], "fish")