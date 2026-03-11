def power(res, result):
    if result == 0:
        return 1
    return res * power(res, result - 1)

print(power(2, 4))
