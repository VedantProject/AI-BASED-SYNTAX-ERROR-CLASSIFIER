def power(num, size):
    if size == 0:
        return 1
    return num * power(num, size - 1)

print(power(10, 3))
