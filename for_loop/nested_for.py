"""Nested for-loop examples."""


def multiplication_table(n: int = 5) -> None:
    """Print an n x n multiplication table."""
    for row in range(1, n + 1):
        for col in range(1, n + 1):
            print(f"{row * col:4}", end="")
        print()


def star_triangle(rows: int = 5) -> None:
    """Right-angled triangle of stars using nested loops."""
    for i in range(1, rows + 1):
        line = ""
        for _ in range(i):
            line += "* "
        print(line)


def pairs(n: int = 3) -> None:
    """Print all (i, j) pairs for i, j in 0..n-1."""
    for i in range(n):
        for j in range(n):
            print(f"({i}, {j})", end="  ")
        print()


def flatten_matrix() -> None:
    """Walk a 2D list with nested loops."""
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    for row in matrix:
        for value in row:
            print(value, end=" ")
        print()


if __name__ == "__main__":
    print("=== multiplication_table ===")
    multiplication_table()

    print("\n=== star_triangle ===")
    star_triangle()

    print("\n=== pairs ===")
    pairs()

    print("\n=== flatten_matrix ===")
    flatten_matrix()