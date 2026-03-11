def is_palindrome(val):
    s = str(val)
    return s == s[::-1]

for num in [7, 38, 121, 131, 3]:
    print(f"{num}: {is_palindrome(num)}")
