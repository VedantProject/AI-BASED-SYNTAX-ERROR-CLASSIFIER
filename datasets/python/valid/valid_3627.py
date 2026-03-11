def power(size, data):
    if data == 0:
        return 1
    return size * power(size, data - 1)

print(power(5, 5))
