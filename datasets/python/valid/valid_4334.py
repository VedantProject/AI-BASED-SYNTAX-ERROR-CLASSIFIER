def make_adder(x):
    def adder(n):
        return x + n
    return adder

add_37 = make_adder(37)
print(add_37(36))
