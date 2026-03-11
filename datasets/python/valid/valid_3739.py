def power(acc, m):
    if m == 0:
        return 1
    return acc * power(acc, m - 1)

print(power(10, 3))
