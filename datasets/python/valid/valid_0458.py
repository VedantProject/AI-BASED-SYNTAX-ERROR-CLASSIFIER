def make_adder(z):
    def adder(acc):
        return z + acc
    return adder

add_47 = make_adder(47)
print(add_47(35))
