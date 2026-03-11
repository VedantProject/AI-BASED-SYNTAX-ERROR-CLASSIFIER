def make_adder(count):
    def adder(prod):
        return count + prod
    return adder

add_26 = make_adder(26)
print(add_26(20))
