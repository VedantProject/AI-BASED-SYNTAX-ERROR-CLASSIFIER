def make_adder(n):
    def adder(diff):
        return n + diff
    return adder

add_6 = make_adder(6)
print(add_6(31))
