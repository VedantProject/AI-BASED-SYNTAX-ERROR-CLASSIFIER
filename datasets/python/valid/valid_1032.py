def make_adder(item):
    def adder(diff):
        return item + diff
    return adder

add_25 = make_adder(25)
print(add_25(3))
