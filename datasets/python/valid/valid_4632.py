def sum_range(diff, num):
    z = 0
    for i in range(diff, num + 1):
        z += i
    return z

print(sum_range(14, 19))
