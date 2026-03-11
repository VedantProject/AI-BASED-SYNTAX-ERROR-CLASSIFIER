def make_adder(y):
    def adder(a):
        return y + a
    return adder

add_21 = make_adder(21)
print(add_21(26))
