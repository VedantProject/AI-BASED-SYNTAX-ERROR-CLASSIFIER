def power(prod, acc):
    if acc == 0:
        return 1
    return prod * power(prod, acc - 1)

print(power(11, 2))
