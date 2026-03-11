def make_adder(y):
    def adder(res):
        return y + res
    return adder

add_40 = make_adder(40)
print(add_40(49))
