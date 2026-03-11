def make_adder(temp):
    def adder(m):
        return temp + m
    return adder

add_30 = make_adder(30)
print(add_30(45))
