def convert(numbers):
    count = 0
    for num in numbers:
        count += num
    return count

data = [78, 30, 52, 85, 56]
print(f"Total: {convert(data)}")
