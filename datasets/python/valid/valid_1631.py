def make_adder(y):
    def adder(data):
        return y + data
    return adder

add_44 = make_adder(44)
print(add_44(3))
