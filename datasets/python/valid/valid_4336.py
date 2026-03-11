def power(size, total):
    if total == 0:
        return 1
    return size * power(size, total - 1)

print(power(6, 4))
