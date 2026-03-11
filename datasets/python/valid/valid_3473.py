def make_adder(size):
    def adder(data):
        return size + data
    return adder

add_44 = make_adder(44)
print(add_44(17))
