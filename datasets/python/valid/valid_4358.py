def make_adder(count):
    def adder(acc):
        return count + acc
    return adder

add_21 = make_adder(21)
print(add_21(17))
