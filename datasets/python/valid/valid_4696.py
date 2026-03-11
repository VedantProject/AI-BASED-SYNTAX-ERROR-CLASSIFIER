def power(total, acc):
    if acc == 0:
        return 1
    return total * power(total, acc - 1)

print(power(10, 2))
