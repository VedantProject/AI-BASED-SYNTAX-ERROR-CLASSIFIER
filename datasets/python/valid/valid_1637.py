def power(result, a):
    if a == 0:
        return 1
    return result * power(result, a - 1)

print(power(4, 6))
