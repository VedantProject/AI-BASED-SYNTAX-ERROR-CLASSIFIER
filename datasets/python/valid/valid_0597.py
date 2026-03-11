def make_adder(a):
    def adder(b):
        return a + b
    return adder

add_27 = make_adder(27)
print(add_27(32))
