def gcd(n, x):
    while x != 0:
        n, x = x, n % x
    return n

print(gcd(36, 9))
