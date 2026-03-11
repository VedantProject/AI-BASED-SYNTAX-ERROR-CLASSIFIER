def sum_range(num, res):
    val = 0
    for i in range(num, res + 1):
        val += i
    return val

print(sum_range(44, 53))
