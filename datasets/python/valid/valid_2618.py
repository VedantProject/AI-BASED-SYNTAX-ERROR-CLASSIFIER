def make_adder(res):
    def adder(val):
        return res + val
    return adder

add_4 = make_adder(4)
print(add_4(33))
