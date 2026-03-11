def solve(numbers):
    res = 0
    for num in numbers:
        res += num
    return res

data = [94, 19, 41, 86]
print(f"Total: {solve(data)}")
