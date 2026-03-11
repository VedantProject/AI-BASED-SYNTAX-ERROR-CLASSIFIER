def power(n, data):
    if data == 0:
        return 1
    return n * power(n, data - 1)

print(power(4, 5))
