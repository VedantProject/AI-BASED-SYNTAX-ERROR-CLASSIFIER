def make_adder(val):
    def adder(total):
        return val + total
    return adder

add_22 = make_adder(22)
print(add_22(43))
