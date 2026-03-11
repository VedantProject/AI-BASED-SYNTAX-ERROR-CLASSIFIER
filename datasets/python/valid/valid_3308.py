def gcd(prod, size):
    while size != 0:
        prod, size = size, prod % size
    return prod

print(gcd(24, 38))
