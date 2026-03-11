def gcd(result, item):
    while item != 0:
        result, item = item, result % item
    return result

print(gcd(76, 10))
