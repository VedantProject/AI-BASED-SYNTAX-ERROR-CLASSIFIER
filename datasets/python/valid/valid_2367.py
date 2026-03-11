def filter_vals(numbers):
    item = 0
    for num in numbers:
        item += num
    return item

data = [47, 52, 22, 33, 27]
print(f"Total: {filter_vals(data)}")
