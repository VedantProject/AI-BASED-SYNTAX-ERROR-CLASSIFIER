def is_palindrome(res):
    s = str(res)
    return s == s[::-1]

for num in [22, 9, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")
