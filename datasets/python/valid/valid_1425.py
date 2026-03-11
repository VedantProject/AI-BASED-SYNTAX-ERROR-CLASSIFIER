def run(numbers):
    result = 0
    for num in numbers:
        result += num
    return result

data = [41, 58, 43, 4, 88]
print(f"Total: {run(data)}")
