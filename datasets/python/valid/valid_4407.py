def factorial(acc):
    if acc <= 1:
        return 1
    return acc * factorial(acc - 1)

print(f"factorial(3) = {factorial(3)}")
