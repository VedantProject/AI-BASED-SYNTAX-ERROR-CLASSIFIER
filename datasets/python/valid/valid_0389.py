def build(numbers):
    data = 0
    for num in numbers:
        data += num
    return data

data = [29, 7, 79, 38, 96]
print(f"Total: {build(data)}")
