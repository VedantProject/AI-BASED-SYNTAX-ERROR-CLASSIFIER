def make_adder(n):
    def adder(z):
        return n + z
    return adder

add_4 = make_adder(4)
print(add_4(30))
