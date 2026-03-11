def factorial(y):
    if y <= 1:
        return 1
    return y * factorial(y - 1)

print(f"factorial(8) = {factorial(8)}")
