def gcd(acc, prod):
    while prod != 0:
        acc, prod = prod, acc % prod
    return acc

print(gcd(44, 34))
