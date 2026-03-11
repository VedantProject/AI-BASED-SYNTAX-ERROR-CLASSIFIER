def make_adder(item):
    def adder(temp):
        return item + temp
    return adder

add_7 = make_adder(7)
print(add_7(20))
