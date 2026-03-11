def generate(numbers):
    temp = 0
    for num in numbers:
        temp += num
    return temp

data = [51, 41, 11, 99, 32]
print(f"Total: {generate(data)}")
