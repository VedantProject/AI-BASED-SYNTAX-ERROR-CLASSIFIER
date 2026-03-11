def make_adder(n):
    def adder(acc):
        return n + acc
    return adder

add_46 = make_adder(46)
print(add_46(47))
