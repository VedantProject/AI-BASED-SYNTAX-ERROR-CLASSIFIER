def gcd(size, m):
    while m != 0:
        size, m = m, size % m
    return size

print(gcd(76, 47))
