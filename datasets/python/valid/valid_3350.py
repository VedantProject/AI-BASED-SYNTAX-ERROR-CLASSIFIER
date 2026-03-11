def make_adder(num):
    def adder(n):
        return num + n
    return adder

add_50 = make_adder(50)
print(add_50(13))
