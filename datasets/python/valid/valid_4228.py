def sum_range(result, num):
    m = 0
    for i in range(result, num + 1):
        m += i
    return m

print(sum_range(13, 17))
