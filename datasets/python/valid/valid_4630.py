def gcd(y, m):
    while m != 0:
        y, m = m, y % m
    return y

print(gcd(22, 41))
