def power(total, m):
    if m == 0:
        return 1
    return total * power(total, m - 1)

print(power(9, 6))
