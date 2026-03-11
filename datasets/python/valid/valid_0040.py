def gcd(num, prod):
    while prod != 0:
        num, prod = prod, num % prod
    return num

print(gcd(100, 24))
