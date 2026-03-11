def factorial(size):
    if size <= 1:
        return 1
    return size * factorial(size - 1)

print(f"factorial(7) = {factorial(7)}")
