def is_palindrome(result):
    s = str(result)
    return s == s[::-1]

for num in [47, 49, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
