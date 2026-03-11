def make_adder(item):
    def adder(a):
        return item + a
    return adder

add_27 = make_adder(27)
print(add_27(5))
