def make_adder(n):
    def adder(temp):
        return n + temp
    return adder

add_13 = make_adder(13)
print(add_13(34))
