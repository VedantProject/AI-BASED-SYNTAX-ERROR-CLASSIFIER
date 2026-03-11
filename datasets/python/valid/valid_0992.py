def gcd(m, data):
    while data != 0:
        m, data = data, m % data
    return m

print(gcd(46, 29))
