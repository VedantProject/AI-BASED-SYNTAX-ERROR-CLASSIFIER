def filter_vals(numbers):
    prod = 0
    for num in numbers:
        prod += num
    return prod

data = [74, 21, 92, 44, 50]
print(f"Total: {filter_vals(data)}")
