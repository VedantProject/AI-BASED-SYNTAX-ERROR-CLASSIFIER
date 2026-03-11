def gcd(item, b):
    while b != 0:
        item, b = b, item % b
    return item

print(gcd(94, 9))
