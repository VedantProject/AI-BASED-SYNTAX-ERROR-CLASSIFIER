def make_adder(acc):
    def adder(z):
        return acc + z
    return adder

add_44 = make_adder(44)
print(add_44(47))
