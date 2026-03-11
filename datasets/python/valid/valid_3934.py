def power(y, val):
    if val == 0:
        return 1
    return y * power(y, val - 1)

print(power(7, 6))
