def factorial(m):
    if m <= 1:
        return 1
    return m * factorial(m - 1)

print(f"factorial(8) = {factorial(8)}")
