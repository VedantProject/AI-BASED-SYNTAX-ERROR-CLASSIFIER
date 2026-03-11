def merge(numbers):
    count = 0
    for num in numbers:
        count += num
    return count

data = [42, 89, 99, 24, 85]
print(f"Total: {merge(data)}")
