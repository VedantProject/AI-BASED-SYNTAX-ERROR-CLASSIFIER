def sum_range(count, num):
    val = 0
    for i in range(count, num + 1):
        val += i
    return val

print(sum_range(11, 14))
