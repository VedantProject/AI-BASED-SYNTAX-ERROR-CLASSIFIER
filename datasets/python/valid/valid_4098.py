def is_palindrome(num):
    s = str(num)
    return s == s[::-1]

for num in [9, 25, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
