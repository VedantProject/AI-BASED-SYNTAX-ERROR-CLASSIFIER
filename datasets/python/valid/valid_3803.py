def gcd(res, val):
    while val != 0:
        res, val = val, res % val
    return res

print(gcd(76, 11))
