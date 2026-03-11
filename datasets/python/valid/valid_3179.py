def make_adder(b):
    def adder(z):
        return b + z
    return adder

add_21 = make_adder(21)
print(add_21(16))
