def make_adder(m):
    def adder(z):
        return m + z
    return adder

add_15 = make_adder(15)
print(add_15(48))
