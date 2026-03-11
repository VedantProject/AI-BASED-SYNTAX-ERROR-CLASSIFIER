def make_adder(y):
    def adder(temp):
        return y + temp
    return adder

add_45 = make_adder(45)
print(add_45(36))
