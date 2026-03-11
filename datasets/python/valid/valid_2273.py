def sum_range(a, z):
    num = 0
    for i in range(a, z + 1):
        num += i
    return num

print(sum_range(42, 46))
