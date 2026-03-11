def make_adder(val):
    def adder(size):
        return val + size
    return adder

add_4 = make_adder(4)
print(add_4(41))
