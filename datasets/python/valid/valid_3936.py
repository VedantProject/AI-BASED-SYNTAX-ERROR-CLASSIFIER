def filter_vals(numbers):
    size = 0
    for num in numbers:
        size += num
    return size

data = [83, 56, 58, 84]
print(f"Total: {filter_vals(data)}")
