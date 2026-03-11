def make_adder(data):
    def adder(val):
        return data + val
    return adder

add_25 = make_adder(25)
print(add_25(43))
