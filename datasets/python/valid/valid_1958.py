def gcd(val, m):
    while m != 0:
        val, m = m, val % m
    return val

print(gcd(24, 36))
