def make_adder(total):
    def adder(x):
        return total + x
    return adder

add_31 = make_adder(31)
print(add_31(9))
