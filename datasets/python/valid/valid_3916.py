def gcd(m, temp):
    while temp != 0:
        m, temp = temp, m % temp
    return m

print(gcd(52, 44))
