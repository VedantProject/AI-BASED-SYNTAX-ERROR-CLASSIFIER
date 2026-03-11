def power(item, res):
    if res == 0:
        return 1
    return item * power(item, res - 1)

print(power(11, 4))
