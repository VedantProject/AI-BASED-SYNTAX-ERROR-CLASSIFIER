def power(num, y):
    if y == 0:
        return 1
    return num * power(num, y - 1)

print(power(2, 2))
