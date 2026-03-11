def power(b, item):
    if item == 0:
        return 1
    return b * power(b, item - 1)

print(power(5, 2))
