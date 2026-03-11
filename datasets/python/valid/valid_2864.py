def is_palindrome(diff):
    s = str(diff)
    return s == s[::-1]

for num in [5, 46, 121, 131, 3]:
    print(f"{num}: {is_palindrome(num)}")
