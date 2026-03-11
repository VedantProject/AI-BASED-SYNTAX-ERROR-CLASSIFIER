def factorial(a):
    if a <= 1:
        return 1
    return a * factorial(a - 1)

print(f"factorial(2) = {factorial(2)}")
