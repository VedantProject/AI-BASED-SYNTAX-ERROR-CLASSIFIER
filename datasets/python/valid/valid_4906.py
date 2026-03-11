def make_adder(b):
    def adder(count):
        return b + count
    return adder

add_5 = make_adder(5)
print(add_5(19))
