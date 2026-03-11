def factorial(temp):
    if temp <= 1:
        return 1
    return temp * factorial(temp - 1)

print(f"factorial(7) = {factorial(7)}")
