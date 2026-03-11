def make_adder(acc):
    def adder(size):
        return acc + size
    return adder

add_18 = make_adder(18)
print(add_18(30))
