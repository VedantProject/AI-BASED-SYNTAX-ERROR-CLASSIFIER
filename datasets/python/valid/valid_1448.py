def make_adder(temp):
    def adder(m):
        return temp + m
    return adder

add_5 = make_adder(5)
print(add_5(15))
