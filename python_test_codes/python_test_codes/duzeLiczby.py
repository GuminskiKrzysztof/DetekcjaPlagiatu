import sys
import os


def czyPierwsza(liczba):
    for x in range(2,liczba):
        if (liczba % x) == 0:
            return False
    return True
def maks(lista):
    max = lista[0]
    for x in lista:
        if x > max:
            max = x
    return max
def potegaNaLiczbe(liczba):
    liczby = liczba.split("^")
    a = int(liczby[0])
    b = int(liczby[1])
    return a**b

def silniaPrzezSilnie(silnieMianownika, silnielicznika, mianownik, licznik):
    gorneSilnie = []
    dolneSilnie = []
    for x in silnielicznika:
        gorneSilnie.append(int(x[:-1]))
    for x in silnieMianownika:
        dolneSilnie.append(int(x[:-1]))
    a = maks(gorneSilnie)
    b = maks(dolneSilnie)
    silnielicznika.remove(str(a) + "!")
    silnieMianownika.remove(str(b) + "!")
    if a >= b:
        for y in range(b+1,a+1):
            licznik.append(y)
    else:
        for y in range(a+1,b+1):
            mianownik.append(y)

def silnia(n):
    if n == 1:
        return 1
    else:
        return n*silnia(n-1)


def nwd(a,b):
    while a != 0 and b != 0:
        if a >= b:
            a = a % b
        else:
            b = b % a
    if a == 0:
        return b
    else:
        return a


os.chdir("input")
gora = []
dol = []
with open(sys.argv[1], "r") as file:
    gora = file.readline().rstrip().split("*")
    dol = file.readline().rstrip().split("*")
licznik = []
mianownik = []
potegiLicznika = []
potegiMianownika = []
silnieLicznika = []
silnieMianownika = []
a = 0
b = 0
for x in gora:
    if '^' in x and '!' in x:
        potegowanie = x.split("^")
        if "!" in potegowanie[0]:
            a = silnia(int(potegowanie[0][:-1]))
        else:
            a = int(potegowanie[0])
        if "!" in potegowanie[1]:
            b = silnia(int(potegowanie[1][:-1]))
        else:
            b = int(potegowanie[1])
        potegiLicznika.append(str(a) + "^" + str(b))
    elif '^' in x:
        potegiLicznika.append(x)
    elif '!' in x:
        silnieLicznika.append(x)
    else:
        licznik.append(int(x))
for x in dol:
    if '^' in x and '!' in x:
        potegowanie = x.split("^")
        if "!" in potegowanie[0]:
            a = silnia(int(potegowanie[0][:-1]))
        else:
            a = int(potegowanie[0])
        if "!" in potegowanie[1]:
            b = silnia(int(potegowanie[1][:-1]))
        else:
            b = int(potegowanie[1])
        potegiMianownika.append(str(a) + "^" + str(b))
    elif '^' in x:
        potegiMianownika.append(x)
    elif '!' in x:
        silnieMianownika.append(x)
    else:
        mianownik.append(int(x))
while len(silnieLicznika) > 0 and len(silnieMianownika) > 0:
    silniaPrzezSilnie(silnieMianownika,silnieLicznika,mianownik,licznik)
for x in silnieLicznika:
    a = int(x[:-1])
    for i in range(2,a+1):
        licznik.append(i)
silnieLicznika.clear()
for x in silnieMianownika:
    a = int(x[:-1])
    for i in range(2,a+1):
        mianownik.append(i)
silnieMianownika.clear()
for x in potegiLicznika:
    a = potegaNaLiczbe(x)
    licznik.append(a)
for x in potegiMianownika:
    a = potegaNaLiczbe(x)
    mianownik.append(a)
liczbyPierwsze = []
for x in range(2,101):
    if czyPierwsza(x):
        liczbyPierwsze.append(x)
dzielnik = 0
for x in range(len(licznik)):
    if licznik[x] not in liczbyPierwsze:
        for y in range(len(mianownik)):
            if mianownik[y] not in liczbyPierwsze:
                while nwd(licznik[x],mianownik[y]) > 1:
                    dzielnik = nwd(licznik[x], mianownik[y])
                    licznik[x] = licznik[x]//dzielnik
                    mianownik[y] = mianownik[y]//dzielnik
kopiaLicznika = licznik
kopiaMianownika = mianownik
licznik = [x for x in kopiaLicznika if x not in kopiaMianownika]
mianownik = [y for y in kopiaMianownika if y not in kopiaLicznika]
wartoscLicznika = 1
wartoscMianownika = 1
for x in licznik:
    wartoscLicznika = wartoscLicznika*x
for x in mianownik:
    wartoscMianownika = wartoscMianownika*x
wynik = wartoscLicznika//wartoscMianownika
os.chdir("..")
os.chdir("output")
with open(sys.argv[1],"a+") as file2:
    file2.write(str(wynik))

