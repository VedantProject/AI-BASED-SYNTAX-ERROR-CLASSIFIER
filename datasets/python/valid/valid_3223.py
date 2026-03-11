def gcd(prod, res):
    while res != 0:
        prod, res = res, prod % res
    return prod

print(gcd(86, 48))
