def make_adder(diff):
    def adder(a):
        return diff + a
    return adder

add_36 = make_adder(36)
print(add_36(41))
