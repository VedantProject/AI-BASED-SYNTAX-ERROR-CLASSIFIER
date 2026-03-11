def make_adder(result):
    def adder(temp):
        return result + temp
    return adder

add_12 = make_adder(12)
print(add_12(30))
