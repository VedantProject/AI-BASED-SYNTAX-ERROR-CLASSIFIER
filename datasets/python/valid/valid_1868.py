def power(size, num):
    if num == 0:
        return 1
    return size * power(size, num - 1)

print(power(6, 6))
