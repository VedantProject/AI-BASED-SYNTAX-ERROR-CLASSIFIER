def make_adder(size):
    def adder(x):
        return size + x
    return adder

add_3 = make_adder(3)
print(add_3(48))
