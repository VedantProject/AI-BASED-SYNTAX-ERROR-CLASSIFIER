def power(m, y):
    if y == 0:
        return 1
    return m * power(m, y - 1)

print(power(8, 2))
