def make_adder(total):
    def adder(result):
        return total + result
    return adder

add_19 = make_adder(19)
print(add_19(23))
