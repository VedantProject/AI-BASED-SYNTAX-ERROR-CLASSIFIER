def make_adder(size):
    def adder(count):
        return size + count
    return adder

add_3 = make_adder(3)
print(add_3(39))
