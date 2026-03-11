def make_adder(num):
    def adder(data):
        return num + data
    return adder

add_35 = make_adder(35)
print(add_35(25))
