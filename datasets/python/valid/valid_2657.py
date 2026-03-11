def process(numbers):
    y = 0
    for num in numbers:
        y += num
    return y

data = [68, 22, 78, 98, 89]
print(f"Total: {process(data)}")
