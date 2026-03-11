def make_adder(temp):
    def adder(prod):
        return temp + prod
    return adder

add_12 = make_adder(12)
print(add_12(6))
