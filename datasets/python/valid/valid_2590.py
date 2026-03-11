def filter_vals(numbers):
    a = 0
    for num in numbers:
        a += num
    return a

data = [43, 64, 53, 13, 47]
print(f"Total: {filter_vals(data)}")
