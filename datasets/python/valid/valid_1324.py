def make_adder(res):
    def adder(num):
        return res + num
    return adder

add_12 = make_adder(12)
print(add_12(17))
