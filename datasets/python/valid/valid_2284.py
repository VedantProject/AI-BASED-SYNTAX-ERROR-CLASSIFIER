def make_adder(data):
    def adder(result):
        return data + result
    return adder

add_8 = make_adder(8)
print(add_8(5))
