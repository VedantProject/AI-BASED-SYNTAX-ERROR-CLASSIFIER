def make_adder(prod):
    def adder(acc):
        return prod + acc
    return adder

add_43 = make_adder(43)
print(add_43(45))
