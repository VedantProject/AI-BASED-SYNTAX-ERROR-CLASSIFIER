def power(result, m):
    if m == 0:
        return 1
    return result * power(result, m - 1)

print(power(7, 5))
