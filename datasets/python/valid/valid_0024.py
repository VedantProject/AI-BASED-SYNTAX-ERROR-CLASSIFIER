def make_adder(item):
    def adder(prod):
        return item + prod
    return adder

add_50 = make_adder(50)
print(add_50(11))
