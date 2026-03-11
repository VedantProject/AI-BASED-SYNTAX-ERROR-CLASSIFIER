def power(diff, num):
    if num == 0:
        return 1
    return diff * power(diff, num - 1)

print(power(5, 6))
