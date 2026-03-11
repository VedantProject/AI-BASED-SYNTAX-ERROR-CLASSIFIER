def gcd(res, item):
    while item != 0:
        res, item = item, res % item
    return res

print(gcd(22, 8))
