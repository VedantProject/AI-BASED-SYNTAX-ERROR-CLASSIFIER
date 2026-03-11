def power(item, size):
    if size == 0:
        return 1
    return item * power(item, size - 1)

print(power(6, 6))
