def process(numbers):
    num = 0
    for num in numbers:
        num += num
    return num

data = [73, 22, 5, 90]
print(f"Total: {process(data)}")
