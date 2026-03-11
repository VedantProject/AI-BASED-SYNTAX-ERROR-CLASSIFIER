def make_adder(count):
    def adder(total):
        return count + total
    return adder

add_31 = make_adder(31)
print(add_31(23))
