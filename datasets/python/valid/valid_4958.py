def make_adder(z):
    def adder(num):
        return z + num
    return adder

add_20 = make_adder(20)
print(add_20(40))
