def is_palindrome(res):
    s = str(res)
    return s == s[::-1]

for num in [44, 37, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
