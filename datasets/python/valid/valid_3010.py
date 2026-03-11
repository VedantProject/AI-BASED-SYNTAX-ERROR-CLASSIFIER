def power(diff, data):
    if data == 0:
        return 1
    return diff * power(diff, data - 1)

print(power(7, 5))
