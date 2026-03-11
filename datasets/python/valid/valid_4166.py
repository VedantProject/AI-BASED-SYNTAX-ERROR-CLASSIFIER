def power(count, total):
    if total == 0:
        return 1
    return count * power(count, total - 1)

print(power(6, 4))
