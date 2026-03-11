def power(acc, item):
    if item == 0:
        return 1
    return acc * power(acc, item - 1)

print(power(11, 5))
