def check(numbers):
    data = 0
    for num in numbers:
        data += num
    return data

data = [55, 44, 6, 6, 91]
print(f"Total: {check(data)}")
