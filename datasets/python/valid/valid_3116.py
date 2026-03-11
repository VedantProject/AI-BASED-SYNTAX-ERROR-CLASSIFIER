def make_adder(num):
    def adder(data):
        return num + data
    return adder

add_40 = make_adder(40)
print(add_40(22))
