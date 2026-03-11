def make_adder(data):
    def adder(a):
        return data + a
    return adder

add_29 = make_adder(29)
print(add_29(30))
