def make_adder(diff):
    def adder(result):
        return diff + result
    return adder

add_49 = make_adder(49)
print(add_49(35))
