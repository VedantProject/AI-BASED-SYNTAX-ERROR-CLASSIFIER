def make_adder(temp):
    def adder(b):
        return temp + b
    return adder

add_17 = make_adder(17)
print(add_17(49))
