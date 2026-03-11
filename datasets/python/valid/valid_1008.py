def make_adder(acc):
    def adder(num):
        return acc + num
    return adder

add_39 = make_adder(39)
print(add_39(9))
