def make_adder(acc):
    def adder(size):
        return acc + size
    return adder

add_48 = make_adder(48)
print(add_48(14))
