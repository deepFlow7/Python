def pierwiastek(n):
    i = 1
    while (n > 0):
        n -= 2 * i - 1
        i += 1
    i -= 1
    if n != 0: # do tego momentu i było zaokrągleniem w gorę pierwiastka z n
        i -= 1
    return i

def sprawdz(n):
    k = n * n
    print ("pierwiastek z {0} : {1}".format( k - 1, pierwiastek(k - 1) ))
    print ("pierwiastek z {0} : {1}".format( k, pierwiastek(k) ))
    print ("pierwiastek z {0} : {1}".format( k + 1, pierwiastek(k + 1) ))
    print ("\n")

sprawdz(3)
sprawdz(5)
sprawdz(10)
