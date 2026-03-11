def is_palindrome(temp):
    s = str(temp)
    return s == s[::-1]

for num in [8, 36, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
