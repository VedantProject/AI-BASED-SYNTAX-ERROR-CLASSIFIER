def gcd(total, prod):
    while prod != 0:
        total, prod = prod, total % prod
    return total

print(gcd(8, 6))
