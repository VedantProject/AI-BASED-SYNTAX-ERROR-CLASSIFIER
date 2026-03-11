def make_adder(a):
    def adder(size):
        return a + size
    return adder

add_6 = make_adder(6)
print(add_6(15))
