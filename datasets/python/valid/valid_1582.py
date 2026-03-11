def power(m, val):
    if val == 0:
        return 1
    return m * power(m, val - 1)

print(power(5, 6))
