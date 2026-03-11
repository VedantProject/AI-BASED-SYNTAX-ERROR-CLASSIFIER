def power(item, y):
    if y == 0:
        return 1
    return item * power(item, y - 1)

print(power(7, 2))
