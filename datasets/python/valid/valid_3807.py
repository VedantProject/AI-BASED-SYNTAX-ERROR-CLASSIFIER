def make_adder(total):
    def adder(b):
        return total + b
    return adder

add_37 = make_adder(37)
print(add_37(24))
