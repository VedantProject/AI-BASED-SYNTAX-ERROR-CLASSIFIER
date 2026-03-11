def factorial(item):
    if item <= 1:
        return 1
    return item * factorial(item - 1)

print(f"factorial(8) = {factorial(8)}")
