def make_adder(item):
    def adder(m):
        return item + m
    return adder

add_2 = make_adder(2)
print(add_2(22))
