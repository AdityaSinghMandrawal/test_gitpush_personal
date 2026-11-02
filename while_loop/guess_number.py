"""Simple number-guess demo using a while loop."""

import random


def play(secret=None, max_tries=5):
    secret = secret if secret is not None else random.randint(1, 10)
    tries = 0
    guess = None
    # Demo mode: auto-guess toward the secret
    low, high = 1, 10
    while tries < max_tries and guess != secret:
        tries += 1
        guess = (low + high) // 2
        print(f"try {tries}: guessed {guess}")
        if guess < secret:
            low = guess + 1
        elif guess > secret:
            high = guess - 1
    print("found!" if guess == secret else "out of tries")


if __name__ == "__main__":
    play(secret=7)
