def gcd(data, b):
    while b != 0:
        data, b = b, data % b
    return data

print(gcd(44, 10))
