def make_adder(acc):
    def adder(total):
        return acc + total
    return adder

add_18 = make_adder(18)
print(add_18(44))
