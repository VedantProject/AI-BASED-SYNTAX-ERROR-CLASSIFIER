def make_adder(acc):
    def adder(a):
        return acc + a
    return adder

add_36 = make_adder(36)
print(add_36(15))
