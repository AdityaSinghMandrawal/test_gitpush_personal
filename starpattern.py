"""Cool star patterns in Python."""


def diamond(n: int = 5) -> None:
    """Centered diamond of stars."""
    for i in range(1, n + 1):
        print(" " * (n - i) + "* " * i)
    for i in range(n - 1, 0, -1):
        print(" " * (n - i) + "* " * i)


def hollow_pyramid(n: int = 6) -> None:
    """Hollow triangle / pyramid."""
    for i in range(1, n + 1):
        spaces = " " * (n - i)
        if i == 1:
            print(spaces + "*")
        elif i == n:
            print("* " * n)
        else:
            print(spaces + "*" + " " * (2 * i - 3) + "*")


def butterfly(n: int = 5) -> None:
    """Butterfly / bow-tie pattern."""
    for i in range(1, n + 1):
        print("*" * i + " " * (2 * (n - i)) + "*" * i)
    for i in range(n - 1, 0, -1):
        print("*" * i + " " * (2 * (n - i)) + "*" * i)


def spiral_square(n: int = 9) -> None:
    """Hollow square spiral of stars."""
    grid = [[" "] * n for _ in range(n)]
    top, left, bottom, right = 0, 0, n - 1, n - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            grid[top][c] = "*"
        top += 1
        for r in range(top, bottom + 1):
            grid[r][right] = "*"
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                grid[bottom][c] = "*"
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                grid[r][left] = "*"
            left += 1
        # leave a one-cell gap so layers don't merge
        top += 1
        left += 1
        bottom -= 1
        right -= 1
    for row in grid:
        print(" ".join(row))


def christmas_tree(levels: int = 4) -> None:
    """Layered Christmas-tree style stars."""
    width = levels * 2 + 1
    for level in range(1, levels + 1):
        for row in range(level + 1):
            stars = 2 * row + 1
            print(" " * ((width - stars) // 2) + "*" * stars)
    trunk = max(1, levels // 2)
    for _ in range(2):
        print(" " * ((width - trunk) // 2) + "|" * trunk)


def heart(n: int = 6) -> None:
    """Two-lobed heart made of stars."""
    for i in range(n // 2, n, 2):
        print(" " * ((n - i) // 2) + "*" * i + " " * (n - i) + "*" * i)
    for i in range(n, 0, -1):
        print(" " * (n - i) + "*" * (2 * i - 1))


if __name__ == "__main__":
    print("=== Diamond ===")
    diamond()
    print("\n=== Hollow Pyramid ===")
    hollow_pyramid()
    print("\n=== Butterfly ===")
    butterfly()
    print("\n=== Spiral Square ===")
    spiral_square()
    print("\n=== Christmas Tree ===")
    christmas_tree()
    print("\n=== Heart ===")
    heart()
