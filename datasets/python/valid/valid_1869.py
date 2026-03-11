def gcd(val, res):
    while res != 0:
        val, res = res, val % res
    return val

print(gcd(44, 25))
