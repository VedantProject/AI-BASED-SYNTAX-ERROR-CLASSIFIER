def make_adder(item):
    def adder(acc):
        return item + acc
    return adder

add_24 = make_adder(24)
print(add_24(50))
