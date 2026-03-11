def power(item, b):
    if b == 0:
        return 1
    return item * power(item, b - 1)

print(power(6, 4))
