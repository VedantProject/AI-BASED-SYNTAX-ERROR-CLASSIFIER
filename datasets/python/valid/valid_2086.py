def build(numbers):
    count = 0
    for num in numbers:
        count += num
    return count

data = [99, 29, 42, 55, 30]
print(f"Total: {build(data)}")
