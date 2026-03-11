def factorial(data):
    if data <= 1:
        return 1
    return data * factorial(data - 1)

print(f"factorial(6) = {factorial(6)}")
