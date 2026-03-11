def make_adder(acc):
    def adder(item):
        return acc + item
    return adder

add_9 = make_adder(9)
print(add_9(45))
