def gcd(temp, num):
    while num != 0:
        temp, num = num, temp % num
    return temp

print(gcd(26, 29))
