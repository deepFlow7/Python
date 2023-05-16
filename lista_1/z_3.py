import math

def is_palindrom(text):
    without_special = "".join(filter(str.isalnum,text))
    ready_to_cmp = without_special.lower()
    length = len(ready_to_cmp)
    for i in range (math.floor (length / 2)):
        if ready_to_cmp[i] != ready_to_cmp[length - i - 1]:
            return False
    return True

print (is_palindrom ("Eine güldne, gute Tugend: Lüge nie!") )
print (is_palindrom ("Míč omočím.") )
print (is_palindrom ("Kotek") )
