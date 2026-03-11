def check(numbers):
    result = 0
    for num in numbers:
        result += num
    return result

data = [33, 80, 61, 83, 14]
print(f"Total: {check(data)}")
