def power(num, prod):
    if prod == 0:
        return 1
    return num * power(num, prod - 1)

print(power(11, 6))
