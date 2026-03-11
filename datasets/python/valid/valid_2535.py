def make_adder(y):
    def adder(n):
        return y + n
    return adder

add_7 = make_adder(7)
print(add_7(31))
