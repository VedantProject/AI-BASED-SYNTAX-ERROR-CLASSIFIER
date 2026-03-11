def build(numbers):
    res = 0
    for num in numbers:
        res += num
    return res

data = [71, 30, 71, 35, 80]
print(f"Total: {build(data)}")
