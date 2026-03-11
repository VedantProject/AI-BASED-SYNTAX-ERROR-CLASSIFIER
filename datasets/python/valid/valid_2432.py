def merge(numbers):
    result = 0
    for num in numbers:
        result += num
    return result

data = [81, 27, 5, 91, 42]
print(f"Total: {merge(data)}")
