def make_adder(total):
    def adder(x):
        return total + x
    return adder

add_29 = make_adder(29)
print(add_29(36))
