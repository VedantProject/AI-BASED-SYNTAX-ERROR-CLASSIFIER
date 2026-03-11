def make_adder(m):
    def adder(val):
        return m + val
    return adder

add_11 = make_adder(11)
print(add_11(38))
