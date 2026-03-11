def power(item, prod):
    if prod == 0:
        return 1
    return item * power(item, prod - 1)

print(power(6, 6))
