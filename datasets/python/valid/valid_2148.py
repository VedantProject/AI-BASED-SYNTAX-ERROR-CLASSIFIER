def solve(numbers):
    item = 0
    for num in numbers:
        item += num
    return item

data = [66, 19, 89, 68, 63]
print(f"Total: {solve(data)}")
