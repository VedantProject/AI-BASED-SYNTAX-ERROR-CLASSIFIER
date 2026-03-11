def check(numbers):
    temp = 0
    for num in numbers:
        temp += num
    return temp

data = [95, 66, 96, 49, 34]
print(f"Total: {check(data)}")
