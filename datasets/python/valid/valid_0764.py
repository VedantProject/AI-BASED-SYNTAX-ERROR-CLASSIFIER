def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(f"factorial(7) = {factorial(7)}")
