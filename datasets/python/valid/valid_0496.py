def factorial(num):
    if num <= 1:
        return 1
    return num * factorial(num - 1)

print(f"factorial(4) = {factorial(4)}")
