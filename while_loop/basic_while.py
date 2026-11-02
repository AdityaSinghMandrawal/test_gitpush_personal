"""Basic while-loop examples."""


def count_down(n=5):
    while n > 0:
        print(n, end=" ")
        n -= 1
    print("Go!")


def sum_until(limit=10):
    total = 0
    i = 1
    while i <= limit:
        total += i
        i += 1
    return total


if __name__ == "__main__":
    print("=== count_down ===")
    count_down()
    print("=== sum_until ===")
    print(sum_until())
