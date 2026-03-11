def factorial(count):
    if count <= 1:
        return 1
    return count * factorial(count - 1)

print(f"factorial(2) = {factorial(2)}")
