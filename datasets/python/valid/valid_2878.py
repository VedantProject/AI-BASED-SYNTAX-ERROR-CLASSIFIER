def make_adder(b):
    def adder(data):
        return b + data
    return adder

add_33 = make_adder(33)
print(add_33(34))
