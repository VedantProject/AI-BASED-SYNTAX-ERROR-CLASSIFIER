def gcd(acc, x):
    while x != 0:
        acc, x = x, acc % x
    return acc

print(gcd(60, 28))
