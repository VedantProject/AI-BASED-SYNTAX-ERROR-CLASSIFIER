def make_adder(size):
    def adder(count):
        return size + count
    return adder

add_43 = make_adder(43)
print(add_43(19))
