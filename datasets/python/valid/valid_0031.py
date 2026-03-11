def gcd(x, res):
    while res != 0:
        x, res = res, x % res
    return x

print(gcd(32, 47))
