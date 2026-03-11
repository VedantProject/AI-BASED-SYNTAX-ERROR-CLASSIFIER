def make_adder(item):
    def adder(val):
        return item + val
    return adder

add_15 = make_adder(15)
print(add_15(36))
