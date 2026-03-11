def make_adder(temp):
    def adder(size):
        return temp + size
    return adder

add_19 = make_adder(19)
print(add_19(23))
