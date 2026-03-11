def make_adder(acc):
    def adder(a):
        return acc + a
    return adder

add_12 = make_adder(12)
print(add_12(43))
