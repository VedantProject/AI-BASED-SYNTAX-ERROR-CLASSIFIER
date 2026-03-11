def generate(numbers):
    a = 0
    for num in numbers:
        a += num
    return a

data = [53, 12, 23, 17, 26]
print(f"Total: {generate(data)}")
