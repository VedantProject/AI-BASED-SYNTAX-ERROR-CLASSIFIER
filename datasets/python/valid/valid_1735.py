def make_adder(temp):
    def adder(item):
        return temp + item
    return adder

add_30 = make_adder(30)
print(add_30(25))
