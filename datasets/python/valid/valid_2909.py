def power(val, temp):
    if temp == 0:
        return 1
    return val * power(val, temp - 1)

print(power(6, 2))
