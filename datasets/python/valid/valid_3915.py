def generate(numbers):
    count = 0
    for num in numbers:
        count += num
    return count

data = [57, 30, 16, 7, 46]
print(f"Total: {generate(data)}")
