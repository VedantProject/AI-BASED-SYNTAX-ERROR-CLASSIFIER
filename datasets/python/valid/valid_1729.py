def make_adder(y):
    def adder(temp):
        return y + temp
    return adder

add_25 = make_adder(25)
print(add_25(20))
