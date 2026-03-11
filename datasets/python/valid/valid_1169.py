def make_adder(x):
    def adder(acc):
        return x + acc
    return adder

add_5 = make_adder(5)
print(add_5(8))
