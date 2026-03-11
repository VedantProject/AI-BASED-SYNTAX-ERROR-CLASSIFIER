def make_adder(data):
    def adder(acc):
        return data + acc
    return adder

add_45 = make_adder(45)
print(add_45(4))
