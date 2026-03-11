def make_adder(temp):
    def adder(acc):
        return temp + acc
    return adder

add_38 = make_adder(38)
print(add_38(44))
