def make_adder(size):
    def adder(m):
        return size + m
    return adder

add_26 = make_adder(26)
print(add_26(25))
