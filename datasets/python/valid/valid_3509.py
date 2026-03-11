def gcd(m, size):
    while size != 0:
        m, size = size, m % size
    return m

print(gcd(26, 36))
