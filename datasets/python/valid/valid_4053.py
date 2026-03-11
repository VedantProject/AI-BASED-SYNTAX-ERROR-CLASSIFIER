def make_adder(y):
    def adder(temp):
        return y + temp
    return adder

add_24 = make_adder(24)
print(add_24(38))
