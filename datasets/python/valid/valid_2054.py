def power(m, diff):
    if diff == 0:
        return 1
    return m * power(m, diff - 1)

print(power(7, 2))
