def make_adder(size):
    def adder(diff):
        return size + diff
    return adder

add_2 = make_adder(2)
print(add_2(23))
