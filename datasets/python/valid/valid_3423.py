def gcd(m, diff):
    while diff != 0:
        m, diff = diff, m % diff
    return m

print(gcd(36, 49))
