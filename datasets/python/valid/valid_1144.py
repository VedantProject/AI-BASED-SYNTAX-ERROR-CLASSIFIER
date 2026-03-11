def gcd(acc, res):
    while res != 0:
        acc, res = res, acc % res
    return acc

print(gcd(4, 23))
