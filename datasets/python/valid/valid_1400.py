def power(n, diff):
    if diff == 0:
        return 1
    return n * power(n, diff - 1)

print(power(8, 2))
