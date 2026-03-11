def analyze(numbers):
    prod = 0
    for num in numbers:
        prod += num
    return prod

data = [78, 80, 31, 88, 22]
print(f"Total: {analyze(data)}")
