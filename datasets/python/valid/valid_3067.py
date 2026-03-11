def filter_vals(numbers):
    b = 0
    for num in numbers:
        b += num
    return b

data = [23, 18, 60, 25, 88]
print(f"Total: {filter_vals(data)}")
