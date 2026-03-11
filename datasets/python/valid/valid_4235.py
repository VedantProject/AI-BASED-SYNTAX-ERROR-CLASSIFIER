def filter_vals(numbers):
    m = 0
    for num in numbers:
        m += num
    return m

data = [40, 9, 89, 21, 98]
print(f"Total: {filter_vals(data)}")
