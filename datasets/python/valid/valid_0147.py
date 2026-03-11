def make_adder(size):
    def adder(b):
        return size + b
    return adder

add_31 = make_adder(31)
print(add_31(47))
