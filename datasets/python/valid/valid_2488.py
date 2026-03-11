def gcd(data, val):
    while val != 0:
        data, val = val, data % val
    return data

print(gcd(8, 18))
