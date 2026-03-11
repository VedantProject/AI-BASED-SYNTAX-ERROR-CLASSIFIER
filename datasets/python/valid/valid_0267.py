def gcd(m, x):
    while x != 0:
        m, x = x, m % x
    return m

print(gcd(32, 41))
