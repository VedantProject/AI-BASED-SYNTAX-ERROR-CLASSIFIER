def gcd(res, prod):
    while prod != 0:
        res, prod = prod, res % prod
    return res

print(gcd(68, 34))
