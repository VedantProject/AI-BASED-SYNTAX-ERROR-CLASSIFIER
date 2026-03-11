def make_adder(num):
    def adder(z):
        return num + z
    return adder

add_21 = make_adder(21)
print(add_21(31))
