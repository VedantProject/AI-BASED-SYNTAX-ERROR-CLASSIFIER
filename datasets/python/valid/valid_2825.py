def filter_vals(numbers):
    n = 0
    for num in numbers:
        n += num
    return n

data = [21, 57, 7, 36, 60]
print(f"Total: {filter_vals(data)}")
