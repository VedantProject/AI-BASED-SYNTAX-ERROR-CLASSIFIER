def sum_range(diff, res):
    b = 0
    for i in range(diff, res + 1):
        b += i
    return b

print(sum_range(39, 41))
