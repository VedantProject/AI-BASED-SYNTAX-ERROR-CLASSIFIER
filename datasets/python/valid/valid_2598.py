def power(item, count):
    if count == 0:
        return 1
    return item * power(item, count - 1)

print(power(3, 4))
