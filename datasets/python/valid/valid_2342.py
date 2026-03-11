def power(diff, m):
    if m == 0:
        return 1
    return diff * power(diff, m - 1)

print(power(4, 3))
