def gcd(y, result):
    while result != 0:
        y, result = result, y % result
    return y

print(gcd(52, 20))
