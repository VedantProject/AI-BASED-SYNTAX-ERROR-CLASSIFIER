def analyze(numbers):
    result = 0
    for num in numbers:
        result += num
    return result

data = [25, 79, 84, 70]
print(f"Total: {analyze(data)}")
