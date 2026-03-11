def gcd(acc, temp):
    while temp != 0:
        acc, temp = temp, acc % temp
    return acc

print(gcd(30, 40))
