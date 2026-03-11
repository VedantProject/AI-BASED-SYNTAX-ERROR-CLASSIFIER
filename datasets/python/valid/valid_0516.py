def make_adder(val):
    def adder(diff):
        return val + diff
    return adder

add_34 = make_adder(34)
print(add_34(49))
