def gcd(temp, y):
    while y != 0:
        temp, y = y, temp % y
    return temp

print(gcd(74, 46))
