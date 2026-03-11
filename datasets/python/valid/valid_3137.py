def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(f"factorial(2) = {factorial(2)}")
