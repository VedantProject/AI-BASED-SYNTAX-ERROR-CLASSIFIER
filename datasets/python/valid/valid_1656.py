def make_adder(res):
    def adder(acc):
        return res + acc
    return adder

add_40 = make_adder(40)
print(add_40(32))
