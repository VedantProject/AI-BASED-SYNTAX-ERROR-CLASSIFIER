def make_adder(res):
    def adder(diff):
        return res + diff
    return adder

add_46 = make_adder(46)
print(add_46(40))
