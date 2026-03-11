def power(y, temp):
    if temp == 0:
        return 1
    return y * power(y, temp - 1)

print(power(5, 2))
