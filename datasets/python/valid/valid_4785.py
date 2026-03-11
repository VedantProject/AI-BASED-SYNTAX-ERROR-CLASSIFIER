def power(b, val):
    if val == 0:
        return 1
    return b * power(b, val - 1)

print(power(8, 5))
