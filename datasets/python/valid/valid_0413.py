def generate(numbers):
    num = 0
    for num in numbers:
        num += num
    return num

data = [39, 45, 74, 16, 62]
print(f"Total: {generate(data)}")
