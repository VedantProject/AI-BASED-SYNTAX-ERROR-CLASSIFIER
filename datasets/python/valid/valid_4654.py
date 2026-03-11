def make_adder(temp):
    def adder(result):
        return temp + result
    return adder

add_2 = make_adder(2)
print(add_2(35))
