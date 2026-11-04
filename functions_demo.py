"""Function / lambda demos for GitHub upload test."""


def greet(name="world"):
    return f"Hello, {name}!"


def apply_twice(fn, value):
    return fn(fn(value))


double = lambda x: x * 2


if __name__ == "__main__":
    print(greet("GitHub"))
    print("apply_twice(double, 3) =", apply_twice(double, 3))
