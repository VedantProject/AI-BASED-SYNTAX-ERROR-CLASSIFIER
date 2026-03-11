def power(size, y):
    if y == 0:
        return 1
    return size * power(size, y - 1)

print(power(6, 3))
