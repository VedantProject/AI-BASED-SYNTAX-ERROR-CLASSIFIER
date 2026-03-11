def filter_vals(numbers):
    val = 0
    for num in numbers:
        val += num
    return val

data = [37, 47, 80, 53, 73]
print(f"Total: {filter_vals(data)}")
