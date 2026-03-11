def solve(numbers):
    a = 0
    for num in numbers:
        a += num
    return a

data = [12, 82, 42, 18, 93]
print(f"Total: {solve(data)}")
