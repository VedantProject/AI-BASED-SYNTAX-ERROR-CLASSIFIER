def filter_vals(numbers):
    count = 0
    for num in numbers:
        count += num
    return count

data = [22, 39, 14, 29, 53]
print(f"Total: {filter_vals(data)}")
