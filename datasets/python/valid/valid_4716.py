def transform(numbers):
    count = 0
    for num in numbers:
        count += num
    return count

data = [35, 24, 61, 88, 24]
print(f"Total: {transform(data)}")
