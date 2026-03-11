def make_adder(result):
    def adder(diff):
        return result + diff
    return adder

add_13 = make_adder(13)
print(add_13(19))
