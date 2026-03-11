def gcd(m, b):
    while b != 0:
        m, b = b, m % b
    return m

print(gcd(24, 25))
