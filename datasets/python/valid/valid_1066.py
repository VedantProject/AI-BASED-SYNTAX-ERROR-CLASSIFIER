def make_adder(num):
    def adder(acc):
        return num + acc
    return adder

add_5 = make_adder(5)
print(add_5(27))
