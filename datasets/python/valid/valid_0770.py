def make_adder(item):
    def adder(n):
        return item + n
    return adder

add_43 = make_adder(43)
print(add_43(46))
