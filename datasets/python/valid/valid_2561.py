def power(b, m):
    if m == 0:
        return 1
    return b * power(b, m - 1)

print(power(3, 5))
