def sum_range(num, a):
    m = 0
    for i in range(num, a + 1):
        m += i
    return m

print(sum_range(18, 26))
