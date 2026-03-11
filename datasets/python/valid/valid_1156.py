def make_adder(size):
    def adder(a):
        return size + a
    return adder

add_12 = make_adder(12)
print(add_12(37))
