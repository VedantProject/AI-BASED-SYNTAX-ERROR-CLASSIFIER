def transform(numbers):
    result = 0
    for num in numbers:
        result += num
    return result

data = [84, 49, 60, 67, 13]
print(f"Total: {transform(data)}")
