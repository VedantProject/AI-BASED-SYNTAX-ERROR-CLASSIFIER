def power(item, temp):
    if temp == 0:
        return 1
    return item * power(item, temp - 1)

print(power(11, 4))
