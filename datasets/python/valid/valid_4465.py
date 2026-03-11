def is_palindrome(num):
    s = str(num)
    return s == s[::-1]

for num in [7, 27, 121, 131, 7]:
    print(f"{num}: {is_palindrome(num)}")
