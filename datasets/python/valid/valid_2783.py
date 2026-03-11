def solve(numbers):
    size = 0
    for num in numbers:
        size += num
    return size

data = [26, 65, 82, 35, 37]
print(f"Total: {solve(data)}")
