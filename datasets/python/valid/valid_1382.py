def check(numbers):
    temp = 0
    for num in numbers:
        temp += num
    return temp

data = [89, 8, 60, 75, 41]
print(f"Total: {check(data)}")
