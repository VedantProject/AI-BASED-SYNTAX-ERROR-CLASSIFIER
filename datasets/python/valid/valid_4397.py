def make_adder(diff):
    def adder(x):
        return diff + x
    return adder

add_25 = make_adder(25)
print(add_25(14))
