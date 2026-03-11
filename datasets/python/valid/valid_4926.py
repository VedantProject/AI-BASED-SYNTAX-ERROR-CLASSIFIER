def make_adder(item):
    def adder(num):
        return item + num
    return adder

add_29 = make_adder(29)
print(add_29(40))
