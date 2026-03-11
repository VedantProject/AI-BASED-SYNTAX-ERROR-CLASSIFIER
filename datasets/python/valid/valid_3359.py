def make_adder(result):
    def adder(res):
        return result + res
    return adder

add_11 = make_adder(11)
print(add_11(9))
