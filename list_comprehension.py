"""Simple list comprehension demos."""


def squares(n=10):
    return [i * i for i in range(1, n + 1)]


def evens(n=20):
    return [i for i in range(1, n + 1) if i % 2 == 0]


def word_lengths(words=None):
    words = words or ["apple", "banana", "cherry"]
    return {w: len(w) for w in words}


if __name__ == "__main__":
    print("squares:", squares())
    print("evens:", evens())
    print("lengths:", word_lengths())
