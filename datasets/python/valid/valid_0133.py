def power(res, data):
    if data == 0:
        return 1
    return res * power(res, data - 1)

print(power(6, 5))
