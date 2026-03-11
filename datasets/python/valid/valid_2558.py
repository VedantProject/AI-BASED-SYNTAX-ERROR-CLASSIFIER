def is_palindrome(acc):
    s = str(acc)
    return s == s[::-1]

for num in [8, 42, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
