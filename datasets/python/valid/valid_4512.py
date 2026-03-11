def make_adder(total):
    def adder(size):
        return total + size
    return adder

add_39 = make_adder(39)
print(add_39(19))
