def make_adder(num):
    def adder(diff):
        return num + diff
    return adder

add_31 = make_adder(31)
print(add_31(10))
