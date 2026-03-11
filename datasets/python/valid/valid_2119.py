def build(numbers):
    n = 0
    for num in numbers:
        n += num
    return n

data = [18, 61, 48, 97, 69]
print(f"Total: {build(data)}")
