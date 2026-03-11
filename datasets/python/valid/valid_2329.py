def make_adder(prod):
    def adder(m):
        return prod + m
    return adder

add_25 = make_adder(25)
print(add_25(4))
