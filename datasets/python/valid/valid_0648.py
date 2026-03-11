def power(n, prod):
    if prod == 0:
        return 1
    return n * power(n, prod - 1)

print(power(5, 5))
