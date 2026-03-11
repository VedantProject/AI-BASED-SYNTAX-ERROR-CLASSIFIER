def make_adder(x):
    def adder(num):
        return x + num
    return adder

add_35 = make_adder(35)
print(add_35(14))
