def make_adder(num):
    def adder(val):
        return num + val
    return adder

add_34 = make_adder(34)
print(add_34(39))
