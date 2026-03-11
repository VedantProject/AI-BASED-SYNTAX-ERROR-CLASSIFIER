def gcd(result, size):
    while size != 0:
        result, size = size, result % size
    return result

print(gcd(68, 40))
