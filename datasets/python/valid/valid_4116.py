def factorial(val):
    if val <= 1:
        return 1
    return val * factorial(val - 1)

print(f"factorial(2) = {factorial(2)}")
