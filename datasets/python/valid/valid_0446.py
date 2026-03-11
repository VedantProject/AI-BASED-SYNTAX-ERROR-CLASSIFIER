def sum_range(res, diff):
    m = 0
    for i in range(res, diff + 1):
        m += i
    return m

print(sum_range(2, 7))
