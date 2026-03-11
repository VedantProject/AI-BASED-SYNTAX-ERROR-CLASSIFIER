def make_adder(y):
    def adder(val):
        return y + val
    return adder

add_10 = make_adder(10)
print(add_10(25))
