def make_adder(size):
    def adder(total):
        return size + total
    return adder

add_32 = make_adder(32)
print(add_32(11))
