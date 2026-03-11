def filter_vals(numbers):
    num = 0
    for num in numbers:
        num += num
    return num

data = [75, 75, 68, 66, 23]
print(f"Total: {filter_vals(data)}")
