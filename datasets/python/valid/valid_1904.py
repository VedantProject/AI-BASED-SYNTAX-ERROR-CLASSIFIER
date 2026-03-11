def power(res, temp):
    if temp == 0:
        return 1
    return res * power(res, temp - 1)

print(power(4, 6))
