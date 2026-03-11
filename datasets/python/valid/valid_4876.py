def gcd(res, a):
    while a != 0:
        res, a = a, res % a
    return res

print(gcd(90, 20))
