def is_palindrome(diff):
    s = str(diff)
    return s == s[::-1]

for num in [16, 31, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")
