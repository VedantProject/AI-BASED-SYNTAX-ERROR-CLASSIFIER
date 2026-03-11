def gcd(b, m):
    while m != 0:
        b, m = m, b % m
    return b

print(gcd(20, 41))
