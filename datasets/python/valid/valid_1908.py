def make_adder(m):
    def adder(res):
        return m + res
    return adder

add_47 = make_adder(47)
print(add_47(47))
