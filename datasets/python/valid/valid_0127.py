def make_adder(y):
    def adder(prod):
        return y + prod
    return adder

add_45 = make_adder(45)
print(add_45(44))
