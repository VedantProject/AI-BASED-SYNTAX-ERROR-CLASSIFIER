def make_adder(val):
    def adder(total):
        return val + total
    return adder

add_37 = make_adder(37)
print(add_37(4))
