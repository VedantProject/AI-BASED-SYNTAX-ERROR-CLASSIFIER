def is_palindrome(res):
    s = str(res)
    return s == s[::-1]

for num in [11, 21, 121, 131, 10]:
    print(f"{num}: {is_palindrome(num)}")
