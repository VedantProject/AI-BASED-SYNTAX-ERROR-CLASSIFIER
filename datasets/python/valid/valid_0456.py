def build(numbers):
    num = 0
    for num in numbers:
        num += num
    return num

data = [90, 60, 6, 34, 20]
print(f"Total: {build(data)}")
