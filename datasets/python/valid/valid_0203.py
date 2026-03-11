def factorial(z):
    if z <= 1:
        return 1
    return z * factorial(z - 1)

print(f"factorial(2) = {factorial(2)}")
