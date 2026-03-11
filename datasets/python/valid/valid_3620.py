def is_palindrome(acc):
    s = str(acc)
    return s == s[::-1]

for num in [11, 35, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
