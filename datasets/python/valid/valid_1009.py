def make_adder(n):
    def adder(x):
        return n + x
    return adder

add_17 = make_adder(17)
print(add_17(15))
