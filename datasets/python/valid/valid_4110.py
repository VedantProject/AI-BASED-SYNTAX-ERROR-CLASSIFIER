def make_adder(item):
    def adder(num):
        return item + num
    return adder

add_38 = make_adder(38)
print(add_38(47))
