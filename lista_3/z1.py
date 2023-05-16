from math import sqrt
import  math
import timeit, functools

def czy_pierwsza(n) :
    if n < 2:
        return False
    for i in range(2, math.floor(sqrt(n) + 1)):
        if n % i == 0:
            return False
    return True

def pierwsze_imperatywna(n):
    primes = []
    for i in range(2,n + 1):
        if czy_pierwsza(i):
            primes.append(i)
    return  primes

def pierwsze_skladana(n):
    return [ x for x in range(1, n + 1) if czy_pierwsza(x)]

def pierwsze_funkcyjna(n):
    return list(filter(czy_pierwsza, range(1, n + 1)))

def wynik_timeit(f, x):
    return round(timeit.timeit(functools.partial(f, x), number = 1000), 6)

def time(n) :
    width = 12
    width_2 = 4
    print ('{0:>{1}}'.format('n', width_2), end='')
    print ('{0:>{1}}'.format(' imperatywna', width), end='')
    print ('{0:>{1}}'.format(' skladana', width), end='')
    print ('{0:>{1}}'.format(' funkcyjna', width))
    for i in range(1, n + 1):
        print (f'{10*i:> {width_2}}', end='')
        print (f'{wynik_timeit(pierwsze_imperatywna, 10 * i):> {width}}', end='')
        print (f'{wynik_timeit(pierwsze_skladana, 10 * i):> {width}}', end='')
        print (f'{wynik_timeit(pierwsze_funkcyjna, 10 * i):> {width}}')   

n = 20
print ("Liczby pierwsze nie większe niż {0}:".format(n))
print ("    * imperatywnie :", end = " ")
print (pierwsze_imperatywna(n))
print ("    * lista składana :", end = " ")
print (pierwsze_skladana(n))
print ("    * funkcyjnie :", end = " ")
print (pierwsze_funkcyjna(n))
print ("\nCzas działania (w sekundach) dla 1000 iteracji:")
time(10) 