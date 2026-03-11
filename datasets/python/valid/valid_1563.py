def check(numbers):
    prod = 0
    for num in numbers:
        prod += num
    return prod

data = [96, 82, 19, 46, 7]
print(f"Total: {check(data)}")
