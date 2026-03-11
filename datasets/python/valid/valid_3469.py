def power(m, prod):
    if prod == 0:
        return 1
    return m * power(m, prod - 1)

print(power(11, 2))
