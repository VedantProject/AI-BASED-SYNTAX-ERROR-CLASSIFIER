def convert(numbers):
    count = 0
    for num in numbers:
        count += num
    return count

data = [96, 84, 5, 80, 9]
print(f"Total: {convert(data)}")
