def make_adder(prod):
    def adder(diff):
        return prod + diff
    return adder

add_19 = make_adder(19)
print(add_19(31))
