def make_adder(num):
    def adder(size):
        return num + size
    return adder

add_46 = make_adder(46)
print(add_46(30))
