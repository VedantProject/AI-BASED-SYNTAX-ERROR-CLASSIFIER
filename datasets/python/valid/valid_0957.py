def make_adder(num):
    def adder(n):
        return num + n
    return adder

add_43 = make_adder(43)
print(add_43(15))
