def make_adder(diff):
    def adder(size):
        return diff + size
    return adder

add_7 = make_adder(7)
print(add_7(34))
