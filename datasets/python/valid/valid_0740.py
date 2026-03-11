def factorial(prod):
    if prod <= 1:
        return 1
    return prod * factorial(prod - 1)

print(f"factorial(10) = {factorial(10)}")
