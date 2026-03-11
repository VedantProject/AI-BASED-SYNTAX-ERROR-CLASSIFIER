def gcd(result, x):
    while x != 0:
        result, x = x, result % x
    return result

print(gcd(88, 35))
