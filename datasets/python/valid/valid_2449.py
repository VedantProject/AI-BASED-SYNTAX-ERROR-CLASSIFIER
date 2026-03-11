def make_adder(z):
    def adder(result):
        return z + result
    return adder

add_48 = make_adder(48)
print(add_48(36))
