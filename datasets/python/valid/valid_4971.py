def filter_vals(numbers):
    res = 0
    for num in numbers:
        res += num
    return res

data = [93, 22, 63, 40, 87]
print(f"Total: {filter_vals(data)}")
