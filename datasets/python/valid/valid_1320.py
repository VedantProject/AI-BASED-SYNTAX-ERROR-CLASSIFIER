def reverse_string(s):
    return s[::-1]

words = ["hello", "python", "code", "test"]
for w in words:
    print(f"{w} -> {reverse_string(w)}")
