def solve(numbers):
    size = 0
    for num in numbers:
        size += num
    return size

data = [16, 7, 92, 6, 48]
print(f"Total: {solve(data)}")
