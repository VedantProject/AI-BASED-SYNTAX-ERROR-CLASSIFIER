def make_adder(res):
    def adder(acc):
        return res + acc
    return adder

add_16 = make_adder(16)
print(add_16(33))
