def is_palindrome(acc):
    s = str(acc)
    return s == s[::-1]

for num in [27, 14, 121, 131, 10]:
    print(f"{num}: {is_palindrome(num)}")
