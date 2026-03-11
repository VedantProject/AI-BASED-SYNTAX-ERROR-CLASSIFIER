def make_adder(acc):
    def adder(val):
        return acc + val
    return adder

add_11 = make_adder(11)
print(add_11(35))
