def is_palindrome(temp):
    s = str(temp)
    return s == s[::-1]

for num in [24, 23, 121, 131, 2]:
    print(f"{num}: {is_palindrome(num)}")
