def filter_vals(numbers):
    n = 0
    for num in numbers:
        n += num
    return n

data = [93, 41, 73, 58, 74]
print(f"Total: {filter_vals(data)}")
