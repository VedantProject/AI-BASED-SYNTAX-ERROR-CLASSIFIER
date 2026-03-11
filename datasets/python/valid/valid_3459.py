def process(numbers):
    n = 0
    for num in numbers:
        n += num
    return n

data = [76, 6, 36, 83]
print(f"Total: {process(data)}")
