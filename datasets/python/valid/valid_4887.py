def power(num, data):
    if data == 0:
        return 1
    return num * power(num, data - 1)

print(power(8, 4))
