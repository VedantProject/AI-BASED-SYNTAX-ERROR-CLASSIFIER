def make_adder(temp):
    def adder(prod):
        return temp + prod
    return adder

add_18 = make_adder(18)
print(add_18(20))
