def make_adder(y):
    def adder(m):
        return y + m
    return adder

add_26 = make_adder(26)
print(add_26(11))
