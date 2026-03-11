def make_adder(num):
    def adder(b):
        return num + b
    return adder

add_40 = make_adder(40)
print(add_40(26))
