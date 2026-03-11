def gcd(res, y):
    while y != 0:
        res, y = y, res % y
    return res

print(gcd(70, 15))
