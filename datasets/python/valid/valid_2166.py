def make_adder(b):
    def adder(diff):
        return b + diff
    return adder

add_47 = make_adder(47)
print(add_47(49))
