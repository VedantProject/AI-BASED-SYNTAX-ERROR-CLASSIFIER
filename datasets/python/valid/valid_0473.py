def process(numbers):
    result = 0
    for num in numbers:
        result += num
    return result

data = [41, 63, 59, 35, 61]
print(f"Total: {process(data)}")
