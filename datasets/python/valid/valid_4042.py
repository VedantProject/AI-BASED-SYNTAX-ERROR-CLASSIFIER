def make_adder(prod):
    def adder(y):
        return prod + y
    return adder

add_6 = make_adder(6)
print(add_6(19))
