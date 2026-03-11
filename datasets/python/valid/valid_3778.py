def power(temp, y):
    if y == 0:
        return 1
    return temp * power(temp, y - 1)

print(power(6, 4))
