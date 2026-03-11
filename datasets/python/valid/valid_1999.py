def make_adder(a):
    def adder(data):
        return a + data
    return adder

add_15 = make_adder(15)
print(add_15(43))
