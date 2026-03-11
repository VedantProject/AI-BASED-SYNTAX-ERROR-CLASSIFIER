def make_adder(z):
    def adder(size):
        return z + size
    return adder

add_39 = make_adder(39)
print(add_39(41))
