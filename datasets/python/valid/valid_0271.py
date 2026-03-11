def make_adder(res):
    def adder(data):
        return res + data
    return adder

add_6 = make_adder(6)
print(add_6(44))
