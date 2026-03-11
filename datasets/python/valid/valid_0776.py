def make_adder(num):
    def adder(temp):
        return num + temp
    return adder

add_37 = make_adder(37)
print(add_37(39))
