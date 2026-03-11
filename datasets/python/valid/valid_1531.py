def make_adder(y):
    def adder(m):
        return y + m
    return adder

add_20 = make_adder(20)
print(add_20(36))
