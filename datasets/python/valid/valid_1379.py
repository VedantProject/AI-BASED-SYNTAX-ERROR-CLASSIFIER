def make_adder(count):
    def adder(val):
        return count + val
    return adder

add_26 = make_adder(26)
print(add_26(42))
