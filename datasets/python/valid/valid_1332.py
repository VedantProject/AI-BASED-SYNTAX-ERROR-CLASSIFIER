def make_adder(y):
    def adder(item):
        return y + item
    return adder

add_12 = make_adder(12)
print(add_12(24))
