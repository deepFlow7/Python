from math import sqrt
import  math
import timeit, functools

def czy_doskonala(n) :
    sum = 0
    s = math.floor(sqrt(n))
    for i in range(2, s + 1):
        if n % i == 0:
            sum += i + n / i
    if s^2 == n:
        sum -= s
    if n > 1:
        sum += 1
    return sum == n

def doskonale_imperatywna(n):
    primes = []
    for i in range(1,n + 1):
        if czy_doskonala(i):
            primes.append(i)
    return  primes

def doskonale_skladana(n):
    return [ x for x in range(1, n + 1) if czy_doskonala(x)]

def f(x, n):
    if x == 1:
        return 1
    if x * x == n:
        return x
    return x + n / x
    
def czy_doskonala_funkcyjnie(n):
    s = sum(map(lambda x: f(x, n), filter(lambda x : n % x == 0, range(1, math.floor(sqrt(n)) + 1))))
    return s == n

def doskonale_funkcyjna(n):
    return list(filter(czy_doskonala_funkcyjnie, range(1, n + 1)))

def wynik_timeit(f, x):
    return round(timeit.timeit(functools.partial(f, x), number = 100), 6)

def time(n, j) :
    width = 12
    width_2 = 6
    print ('{0:>{1}}'.format('n', width_2), end='')
    print ('{0:>{1}}'.format(' imperatywna', width), end='')
    print ('{0:>{1}}'.format(' skladana', width), end='')
    print ('{0:>{1}}'.format(' funkcyjna', width))
    for i in range(1, n + 1):
        x = j * i
        print (f'{x:> {width_2}}', end='')
        print (f'{wynik_timeit(doskonale_imperatywna, x):> {width}}', end='')
        print (f'{wynik_timeit(doskonale_skladana, x):> {width}}', end='')
        print (f'{wynik_timeit(doskonale_funkcyjna, x):> {width}}')   

n = 10000
print ("Liczby doskonałe nie większe niż {0}:".format(n))
print ("    * imperatywnie :", end = " ")
print (doskonale_imperatywna(n))
print ("    * lista składana :", end = " ")
print (doskonale_skladana(n))
print ("    * funkcyjnie :", end = " ")
print (doskonale_funkcyjna(n))
print ("\nCzas działania (w sekundach) dla 100 iteracji:")
time(10, 500) 