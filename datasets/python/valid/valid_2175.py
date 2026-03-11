def power(data, n):
    if n == 0:
        return 1
    return data * power(data, n - 1)

print(power(9, 5))
