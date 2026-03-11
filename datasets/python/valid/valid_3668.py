def gcd(count, res):
    while res != 0:
        count, res = res, count % res
    return count

print(gcd(36, 44))
