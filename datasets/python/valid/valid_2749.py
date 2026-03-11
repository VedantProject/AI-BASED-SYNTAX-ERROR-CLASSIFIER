def make_adder(b):
    def adder(temp):
        return b + temp
    return adder

add_8 = make_adder(8)
print(add_8(44))
