def make_adder(prod):
    def adder(acc):
        return prod + acc
    return adder

add_32 = make_adder(32)
print(add_32(9))
