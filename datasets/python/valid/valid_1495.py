def make_adder(temp):
    def adder(acc):
        return temp + acc
    return adder

add_43 = make_adder(43)
print(add_43(37))
