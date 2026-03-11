def make_adder(y):
    def adder(m):
        return y + m
    return adder

add_30 = make_adder(30)
print(add_30(26))
