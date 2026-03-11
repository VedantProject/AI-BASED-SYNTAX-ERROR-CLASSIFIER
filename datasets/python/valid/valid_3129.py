def gcd(y, x):
    while x != 0:
        y, x = x, y % x
    return y

print(gcd(76, 16))
