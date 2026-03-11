def sum_range(data, prod):
    val = 0
    for i in range(data, prod + 1):
        val += i
    return val

print(sum_range(33, 35))
