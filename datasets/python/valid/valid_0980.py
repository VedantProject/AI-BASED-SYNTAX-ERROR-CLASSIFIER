def run(numbers):
    temp = 0
    for num in numbers:
        temp += num
    return temp

data = [92, 25, 19, 90]
print(f"Total: {run(data)}")
