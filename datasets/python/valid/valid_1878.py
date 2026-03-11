def make_adder(diff):
    def adder(total):
        return diff + total
    return adder

add_26 = make_adder(26)
print(add_26(47))
