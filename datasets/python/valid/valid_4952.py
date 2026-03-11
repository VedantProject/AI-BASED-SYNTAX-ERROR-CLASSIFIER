def factorial(num):
    if num <= 1:
        return 1
    return num * factorial(num - 1)

print(f"factorial(6) = {factorial(6)}")
