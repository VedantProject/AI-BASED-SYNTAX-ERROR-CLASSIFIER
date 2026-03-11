def make_adder(size):
    def adder(x):
        return size + x
    return adder

add_47 = make_adder(47)
print(add_47(23))
