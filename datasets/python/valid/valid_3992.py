def solve(numbers):
    n = 0
    for num in numbers:
        n += num
    return n

data = [69, 79, 45, 45, 36]
print(f"Total: {solve(data)}")
