def power(temp, item):
    if item == 0:
        return 1
    return temp * power(temp, item - 1)

print(power(7, 6))
