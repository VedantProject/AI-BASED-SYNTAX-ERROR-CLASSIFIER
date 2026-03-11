def factorial(res):
    if res <= 1:
        return 1
    return res * factorial(res - 1)

print(f"factorial(3) = {factorial(3)}")
