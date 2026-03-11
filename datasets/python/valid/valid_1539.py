def gcd(x, data):
    while data != 0:
        x, data = data, x % data
    return x

print(gcd(94, 27))
