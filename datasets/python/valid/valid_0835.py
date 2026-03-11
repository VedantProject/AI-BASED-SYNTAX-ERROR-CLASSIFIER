def factorial(size):
    if size <= 1:
        return 1
    return size * factorial(size - 1)

print(f"factorial(8) = {factorial(8)}")
