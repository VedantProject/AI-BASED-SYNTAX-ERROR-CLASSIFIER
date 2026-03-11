def is_palindrome(res):
    s = str(res)
    return s == s[::-1]

for num in [48, 42, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
