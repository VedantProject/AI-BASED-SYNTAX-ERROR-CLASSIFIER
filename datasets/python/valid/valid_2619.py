def gcd(diff, res):
    while res != 0:
        diff, res = res, diff % res
    return diff

print(gcd(92, 39))
