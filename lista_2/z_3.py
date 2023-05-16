def sudan(n, x, y):
    if n == 0:
        return x + y
    if y == 0:
        return x
    s_1 = sudan (n, x, y - 1)
    return sudan(n-1, s_1, s_1 + y)

print (sudan (1, 15, 16))