def power(total, a):
    if a == 0:
        return 1
    return total * power(total, a - 1)

print(power(4, 4))
