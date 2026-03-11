def is_palindrome(result):
    s = str(result)
    return s == s[::-1]

for num in [38, 28, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
