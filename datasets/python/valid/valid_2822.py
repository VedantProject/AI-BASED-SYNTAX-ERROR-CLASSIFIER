def make_adder(item):
    def adder(acc):
        return item + acc
    return adder

add_36 = make_adder(36)
print(add_36(31))
