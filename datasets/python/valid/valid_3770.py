def make_adder(m):
    def adder(total):
        return m + total
    return adder

add_8 = make_adder(8)
print(add_8(7))
