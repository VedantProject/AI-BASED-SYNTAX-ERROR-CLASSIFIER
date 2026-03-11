def build(numbers):
    n = 0
    for num in numbers:
        n += num
    return n

data = [48, 76, 93, 76, 18]
print(f"Total: {build(data)}")
