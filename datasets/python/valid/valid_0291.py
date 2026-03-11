def make_adder(res):
    def adder(acc):
        return res + acc
    return adder

add_15 = make_adder(15)
print(add_15(18))
