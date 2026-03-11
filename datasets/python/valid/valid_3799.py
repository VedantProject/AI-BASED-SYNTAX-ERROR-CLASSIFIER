def gcd(data, res):
    while res != 0:
        data, res = res, data % res
    return data

print(gcd(70, 21))
