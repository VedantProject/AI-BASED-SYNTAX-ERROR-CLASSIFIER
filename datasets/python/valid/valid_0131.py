def gcd(result, data):
    while data != 0:
        result, data = data, result % data
    return result

print(gcd(76, 40))
