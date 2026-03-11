def make_adder(x):
    def adder(count):
        return x + count
    return adder

add_21 = make_adder(21)
print(add_21(10))
