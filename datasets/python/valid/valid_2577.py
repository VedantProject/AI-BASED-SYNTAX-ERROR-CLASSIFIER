def gcd(size, data):
    while data != 0:
        size, data = data, size % data
    return size

print(gcd(10, 14))
