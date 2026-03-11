def make_adder(total):
    def adder(size):
        return total + size
    return adder

add_15 = make_adder(15)
print(add_15(31))
