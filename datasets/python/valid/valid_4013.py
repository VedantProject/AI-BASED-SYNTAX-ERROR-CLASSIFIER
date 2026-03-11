def power(y, data):
    if data == 0:
        return 1
    return y * power(y, data - 1)

print(power(9, 2))
