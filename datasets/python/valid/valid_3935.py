def make_adder(res):
    def adder(temp):
        return res + temp
    return adder

add_8 = make_adder(8)
print(add_8(24))
