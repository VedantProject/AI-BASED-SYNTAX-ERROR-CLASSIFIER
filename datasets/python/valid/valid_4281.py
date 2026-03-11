def build(numbers):
    y = 0
    for num in numbers:
        y += num
    return y

data = [30, 57, 59, 5]
print(f"Total: {build(data)}")
