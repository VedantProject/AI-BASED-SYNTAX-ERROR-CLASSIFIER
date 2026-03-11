def gcd(diff, x):
    while x != 0:
        diff, x = x, diff % x
    return diff

print(gcd(78, 8))
