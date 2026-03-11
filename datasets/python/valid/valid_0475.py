def make_adder(z):
    def adder(x):
        return z + x
    return adder

add_11 = make_adder(11)
print(add_11(7))
