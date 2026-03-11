def factorial(temp):
    if temp <= 1:
        return 1
    return temp * factorial(temp - 1)

print(f"factorial(6) = {factorial(6)}")
