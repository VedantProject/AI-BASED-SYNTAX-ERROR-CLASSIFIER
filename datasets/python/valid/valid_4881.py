def factorial(y):
    if y <= 1:
        return 1
    return y * factorial(y - 1)

print(f"factorial(3) = {factorial(3)}")
