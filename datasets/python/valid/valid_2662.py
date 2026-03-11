def process(numbers):
    a = 0
    for num in numbers:
        a += num
    return a

data = [12, 86, 19, 41, 56]
print(f"Total: {process(data)}")
