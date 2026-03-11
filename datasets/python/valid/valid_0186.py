def gcd(result, temp):
    while temp != 0:
        result, temp = temp, result % temp
    return result

print(gcd(46, 37))
