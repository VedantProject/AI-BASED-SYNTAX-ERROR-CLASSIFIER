def gcd(data, acc):
    while acc != 0:
        data, acc = acc, data % acc
    return data

print(gcd(44, 38))
