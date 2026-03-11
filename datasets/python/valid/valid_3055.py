def gcd(prod, n):
    while n != 0:
        prod, n = n, prod % n
    return prod

print(gcd(58, 42))
