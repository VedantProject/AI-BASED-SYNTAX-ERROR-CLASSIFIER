def factorial(total):
    if total <= 1:
        return 1
    return total * factorial(total - 1)

print(f"factorial(6) = {factorial(6)}")
