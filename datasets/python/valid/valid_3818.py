def make_adder(a):
    def adder(acc):
        return a + acc
    return adder

add_21 = make_adder(21)
print(add_21(19))
