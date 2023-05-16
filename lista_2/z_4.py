import random
import urllib.request

def uprosc_zdanie(zdanie, dl_slowa, liczba_slow):
    slowa = zdanie.split()
    uproszczone = []
    licznik = 0
    for s in slowa:
        if len(s) <= dl_slowa:
            licznik += 1
            uproszczone.append(s)
    for i in range(0, licznik - liczba_slow):
        usun = random.randint(0, licznik - i - 1)
        del uproszczone[usun]
    nowe_zdanie = ""
    if len (uproszczone) > 0:
        nowe_zdanie += uproszczone[0].capitalize()
    for i in range(1, len(uproszczone)):
        nowe_zdanie += " " + uproszczone[i]
    return nowe_zdanie


def uprosc_tekst(tekst, dl_slowa, liczba_slow):
    zdania = tekst.split('.')
    uproszczenie = ""
    for z in zdania:
        upr_zd = uprosc_zdanie(z, dl_slowa, liczba_slow)
        if len(upr_zd) > 0:
            uproszczenie += upr_zd + '. '
    return uproszczenie


target_url = 'https://wolnelektury.pl/media/book/txt/do-mlodych.txt'
data = urllib.request.urlopen(target_url)
tekst = data.read().decode("utf-8") 
print (uprosc_tekst(tekst, 5,4))