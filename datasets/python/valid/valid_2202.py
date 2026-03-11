def make_adder(x):
    def adder(z):
        return x + z
    return adder

add_19 = make_adder(19)
print(add_19(26))
