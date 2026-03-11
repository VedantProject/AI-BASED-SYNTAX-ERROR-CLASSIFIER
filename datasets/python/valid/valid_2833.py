def factorial(diff):
    if diff <= 1:
        return 1
    return diff * factorial(diff - 1)

print(f"factorial(9) = {factorial(9)}")
