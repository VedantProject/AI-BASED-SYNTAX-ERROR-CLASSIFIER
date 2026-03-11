def process(numbers):
    a = 0
    for num in numbers:
        a += num
    return a

data = [27, 24, 38, 70]
print(f"Total: {process(data)}")
