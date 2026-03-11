def make_adder(prod):
    def adder(count):
        return prod + count
    return adder

add_47 = make_adder(47)
print(add_47(28))
