def gcd(n, y):
    while y != 0:
        n, y = y, n % y
    return n

print(gcd(26, 46))
