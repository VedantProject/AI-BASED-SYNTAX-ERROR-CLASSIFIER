def make_adder(total):
    def adder(z):
        return total + z
    return adder

add_14 = make_adder(14)
print(add_14(19))
