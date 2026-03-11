def power(res, b):
    if b == 0:
        return 1
    return res * power(res, b - 1)

print(power(10, 4))
