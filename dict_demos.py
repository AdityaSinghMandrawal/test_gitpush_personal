"""Dictionary demos for GitHub upload test."""


def merge_scores(a=None, b=None):
    a = a or {"alice": 10, "bob": 12}
    b = b or {"bob": 5, "cara": 8}
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + v
    return out


def invert(mapping=None):
    mapping = mapping or {"a": 1, "b": 2, "c": 3}
    return {v: k for k, v in mapping.items()}


if __name__ == "__main__":
    print("merged:", merge_scores())
    print("inverted:", invert())
