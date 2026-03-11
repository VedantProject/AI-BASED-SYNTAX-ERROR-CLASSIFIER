def solve(numbers):
    res = 0
    for num in numbers:
        res += num
    return res

data = [58, 83, 42, 59, 58]
print(f"Total: {solve(data)}")
