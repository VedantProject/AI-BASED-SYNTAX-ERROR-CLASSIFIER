def factorial(result):
    if result <= 1:
        return 1
    return result * factorial(result - 1)

print(f"factorial(5) = {factorial(5)}")
