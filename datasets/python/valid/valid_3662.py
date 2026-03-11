def make_adder(prod):
    def adder(temp):
        return prod + temp
    return adder

add_15 = make_adder(15)
print(add_15(11))
