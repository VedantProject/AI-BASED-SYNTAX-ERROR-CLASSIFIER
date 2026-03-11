def make_adder(num):
    def adder(item):
        return num + item
    return adder

add_34 = make_adder(34)
print(add_34(8))
