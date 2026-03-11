def power(size, diff):
    if diff == 0:
        return 1
    return size * power(size, diff - 1)

print(power(10, 4))
