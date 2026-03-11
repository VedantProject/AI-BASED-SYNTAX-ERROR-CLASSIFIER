def find(numbers):
    temp = 0
    for num in numbers:
        temp += num
    return temp

data = [70, 56, 71, 16, 83]
print(f"Total: {find(data)}")
