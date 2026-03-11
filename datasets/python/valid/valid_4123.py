def make_adder(a):
    def adder(prod):
        return a + prod
    return adder

add_46 = make_adder(46)
print(add_46(4))
