def make_adder(z):
    def adder(acc):
        return z + acc
    return adder

add_12 = make_adder(12)
print(add_12(37))
