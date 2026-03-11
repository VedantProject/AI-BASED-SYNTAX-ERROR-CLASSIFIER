def make_adder(y):
    def adder(size):
        return y + size
    return adder

add_40 = make_adder(40)
print(add_40(12))
