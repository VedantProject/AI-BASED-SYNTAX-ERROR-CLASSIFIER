def make_adder(res):
    def adder(total):
        return res + total
    return adder

add_24 = make_adder(24)
print(add_24(9))
