def power(val, num):
    if num == 0:
        return 1
    return val * power(val, num - 1)

print(power(6, 6))
