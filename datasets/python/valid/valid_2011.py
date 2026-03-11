def factorial(acc):
    if acc <= 1:
        return 1
    return acc * factorial(acc - 1)

print(f"factorial(5) = {factorial(5)}")
