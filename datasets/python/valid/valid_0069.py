def filter_vals(numbers):
    y = 0
    for num in numbers:
        y += num
    return y

data = [72, 71, 57, 19, 53]
print(f"Total: {filter_vals(data)}")
