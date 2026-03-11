def make_adder(num):
    def adder(x):
        return num + x
    return adder

add_22 = make_adder(22)
print(add_22(20))
