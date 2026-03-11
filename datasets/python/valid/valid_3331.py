def make_adder(m):
    def adder(b):
        return m + b
    return adder

add_34 = make_adder(34)
print(add_34(18))
