def gcd(size, count):
    while count != 0:
        size, count = count, size % count
    return size

print(gcd(66, 21))
