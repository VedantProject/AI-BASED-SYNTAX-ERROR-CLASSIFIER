def power(data, m):
    if m == 0:
        return 1
    return data * power(data, m - 1)

print(power(4, 3))
