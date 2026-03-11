def factorial(z):
    if z <= 1:
        return 1
    return z * factorial(z - 1)

print(f"factorial(7) = {factorial(7)}")
