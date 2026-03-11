def gcd(result, b):
    while b != 0:
        result, b = b, result % b
    return result

print(gcd(74, 24))
