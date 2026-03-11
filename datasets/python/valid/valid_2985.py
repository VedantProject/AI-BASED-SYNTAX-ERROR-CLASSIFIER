def gcd(prod, data):
    while data != 0:
        prod, data = data, prod % data
    return prod

print(gcd(8, 17))
