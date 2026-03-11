def gcd(res, result):
    while result != 0:
        res, result = result, res % result
    return res

print(gcd(74, 22))
