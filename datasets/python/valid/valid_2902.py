def power(size, prod):
    if prod == 0:
        return 1
    return size * power(size, prod - 1)

print(power(6, 6))
