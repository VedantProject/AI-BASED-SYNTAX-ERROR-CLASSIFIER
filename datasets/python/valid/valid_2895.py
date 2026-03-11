def factorial(prod):
    if prod <= 1:
        return 1
    return prod * factorial(prod - 1)

print(f"factorial(4) = {factorial(4)}")
