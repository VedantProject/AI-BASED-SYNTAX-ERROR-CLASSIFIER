def gcd(item, count):
    while count != 0:
        item, count = count, item % count
    return item

print(gcd(72, 8))
