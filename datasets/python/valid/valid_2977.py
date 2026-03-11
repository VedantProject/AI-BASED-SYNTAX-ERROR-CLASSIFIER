def power(num, diff):
    if diff == 0:
        return 1
    return num * power(num, diff - 1)

print(power(11, 2))
