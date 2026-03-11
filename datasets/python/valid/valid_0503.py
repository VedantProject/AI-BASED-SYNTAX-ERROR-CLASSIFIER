def make_adder(n):
    def adder(b):
        return n + b
    return adder

add_29 = make_adder(29)
print(add_29(46))
