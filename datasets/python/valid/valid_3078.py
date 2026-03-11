def make_adder(a):
    def adder(item):
        return a + item
    return adder

add_9 = make_adder(9)
print(add_9(45))
