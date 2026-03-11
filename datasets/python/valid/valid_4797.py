def gcd(a, m):
    while m != 0:
        a, m = m, a % m
    return a

print(gcd(42, 38))
