def is_palindrome(acc):
    s = str(acc)
    return s == s[::-1]

for num in [35, 24, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")
