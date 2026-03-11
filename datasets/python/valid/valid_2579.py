def gcd(data, count):
    while count != 0:
        data, count = count, data % count
    return data

print(gcd(72, 7))
