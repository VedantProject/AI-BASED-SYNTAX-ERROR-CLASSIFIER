def gcd(res, x):
    while x != 0:
        res, x = x, res % x
    return res

print(gcd(82, 40))
