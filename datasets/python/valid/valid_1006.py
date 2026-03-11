def make_adder(data):
    def adder(y):
        return data + y
    return adder

add_2 = make_adder(2)
print(add_2(15))
