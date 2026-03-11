def filter_vals(numbers):
    prod = 0
    for num in numbers:
        prod += num
    return prod

data = [87, 95, 37, 92, 37]
print(f"Total: {filter_vals(data)}")
