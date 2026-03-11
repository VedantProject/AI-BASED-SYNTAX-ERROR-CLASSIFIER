def gcd(acc, m):
    while m != 0:
        acc, m = m, acc % m
    return acc

print(gcd(72, 39))
