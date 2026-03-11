def collect(numbers):
    temp = 0
    for num in numbers:
        temp += num
    return temp

data = [64, 60, 4, 44, 5]
print(f"Total: {collect(data)}")
