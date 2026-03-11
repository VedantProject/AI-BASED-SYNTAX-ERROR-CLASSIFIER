def make_adder(temp):
    def adder(result):
        return temp + result
    return adder

add_9 = make_adder(9)
print(add_9(21))
