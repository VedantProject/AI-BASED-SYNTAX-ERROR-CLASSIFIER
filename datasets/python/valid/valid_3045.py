def transform(numbers):
    count = 0
    for num in numbers:
        count += num
    return count

data = [88, 81, 1, 34, 64]
print(f"Total: {transform(data)}")
