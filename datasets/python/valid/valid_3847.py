def gcd(temp, item):
    while item != 0:
        temp, item = item, temp % item
    return temp

print(gcd(42, 5))
