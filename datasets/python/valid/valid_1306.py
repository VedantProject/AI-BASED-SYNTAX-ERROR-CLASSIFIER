def power(res, diff):
    if diff == 0:
        return 1
    return res * power(res, diff - 1)

print(power(4, 5))
