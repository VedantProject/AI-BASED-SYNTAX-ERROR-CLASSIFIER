def is_palindrome(num):
    s = str(num)
    return s == s[::-1]

for num in [19, 28, 121, 131, 10]:
    print(f"{num}: {is_palindrome(num)}")
