def power(count, n):
    if n == 0:
        return 1
    return count * power(count, n - 1)

print(power(3, 2))
