def is_palindrome(temp):
    s = str(temp)
    return s == s[::-1]

for num in [10, 30, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
