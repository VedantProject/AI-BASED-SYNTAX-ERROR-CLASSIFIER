def sum_range(total, a):
    diff = 0
    for i in range(total, a + 1):
        diff += i
    return diff

print(sum_range(15, 22))
