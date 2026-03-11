def power(item, acc):
    if acc == 0:
        return 1
    return item * power(item, acc - 1)

print(power(6, 4))
