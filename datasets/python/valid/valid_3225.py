def make_adder(count):
    def adder(a):
        return count + a
    return adder

add_32 = make_adder(32)
print(add_32(22))
