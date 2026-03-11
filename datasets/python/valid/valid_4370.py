def make_adder(acc):
    def adder(temp):
        return acc + temp
    return adder

add_33 = make_adder(33)
print(add_33(35))
