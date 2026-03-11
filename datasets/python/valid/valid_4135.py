def factorial(count):
    if count <= 1:
        return 1
    return count * factorial(count - 1)

print(f"factorial(9) = {factorial(9)}")
