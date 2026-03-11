def find(numbers):
    m = 0
    for num in numbers:
        m += num
    return m

data = [94, 19, 6, 87, 82]
print(f"Total: {find(data)}")
