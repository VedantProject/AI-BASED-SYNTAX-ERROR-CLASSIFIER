def power(diff, total):
    if total == 0:
        return 1
    return diff * power(diff, total - 1)

print(power(10, 2))
