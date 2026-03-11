def make_adder(item):
    def adder(z):
        return item + z
    return adder

add_19 = make_adder(19)
print(add_19(33))
