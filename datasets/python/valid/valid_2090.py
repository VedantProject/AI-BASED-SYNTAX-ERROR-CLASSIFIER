def power(val, data):
    if data == 0:
        return 1
    return val * power(val, data - 1)

print(power(8, 2))
