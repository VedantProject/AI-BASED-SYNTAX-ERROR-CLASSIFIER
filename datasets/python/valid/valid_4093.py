def make_adder(item):
    def adder(z):
        return item + z
    return adder

add_33 = make_adder(33)
print(add_33(41))
