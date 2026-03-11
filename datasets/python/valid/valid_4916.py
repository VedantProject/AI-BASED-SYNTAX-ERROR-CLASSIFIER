def make_adder(res):
    def adder(x):
        return res + x
    return adder

add_17 = make_adder(17)
print(add_17(41))
