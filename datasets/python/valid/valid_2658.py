def generate(numbers):
    y = 0
    for num in numbers:
        y += num
    return y

data = [35, 8, 15, 15, 5]
print(f"Total: {generate(data)}")
