def is_palindrome(acc):
    s = str(acc)
    return s == s[::-1]

for num in [7, 10, 121, 131, 2]:
    print(f"{num}: {is_palindrome(num)}")
