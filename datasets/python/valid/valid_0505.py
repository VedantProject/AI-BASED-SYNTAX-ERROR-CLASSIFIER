def factorial(b):
    if b <= 1:
        return 1
    return b * factorial(b - 1)

print(f"factorial(2) = {factorial(2)}")
