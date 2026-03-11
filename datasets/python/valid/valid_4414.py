def gcd(n, prod):
    while prod != 0:
        n, prod = prod, n % prod
    return n

print(gcd(42, 38))
