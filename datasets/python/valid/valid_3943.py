def sum_range(b, x):
    val = 0
    for i in range(b, x + 1):
        val += i
    return val

print(sum_range(19, 21))
