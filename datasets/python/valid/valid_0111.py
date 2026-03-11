def make_adder(m):
    def adder(result):
        return m + result
    return adder

add_14 = make_adder(14)
print(add_14(46))
