def gcd(a, res):
    while res != 0:
        a, res = res, a % res
    return a

print(gcd(32, 4))
