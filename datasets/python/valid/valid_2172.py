def make_adder(acc):
    def adder(n):
        return acc + n
    return adder

add_22 = make_adder(22)
print(add_22(43))
