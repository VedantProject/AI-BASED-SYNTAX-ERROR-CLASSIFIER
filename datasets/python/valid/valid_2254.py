def power(n, acc):
    if acc == 0:
        return 1
    return n * power(n, acc - 1)

print(power(5, 6))
